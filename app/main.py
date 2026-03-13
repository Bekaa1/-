from __future__ import annotations

import hashlib
import re
from datetime import datetime, timezone
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from app.amo import AmoClient
from app.config import settings
from app.db import Base, SessionLocal, engine
from app.logic import ALLOWED_QUANTITIES, build_due_timestamps, stage_allowed_quantities
from app.models import HookEvent, TaskRecord
from app.notify import send_telegram_message

app = FastAPI(title="amo hooks scheduler")
amo_client = AmoClient()

STATUS_PATTERN = re.compile(r"leads\[status\]\[(\d+)\]\[(id|status_id|pipeline_id|updated_at)\]")


@app.on_event("startup")
def startup() -> None:
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


def parse_status_updates(form_data: dict[str, str]) -> list[dict[str, Any]]:
    chunks: dict[str, dict[str, Any]] = {}
    for key, value in form_data.items():
        match = STATUS_PATTERN.fullmatch(key)
        if not match:
            continue
        idx, field_name = match.groups()
        chunks.setdefault(idx, {})[field_name] = value

    out: list[dict[str, Any]] = []
    for row in chunks.values():
        if "id" in row and "status_id" in row:
            out.append(
                {
                    "lead_id": int(row["id"]),
                    "stage_id": int(row["status_id"]),
                    "pipeline_id": int(row.get("pipeline_id", "0")),
                    "updated_at": int(row.get("updated_at", "0")),
                }
            )
    return out


def extract_quantity(lead: dict[str, Any]) -> int | None:
    for field in lead.get("custom_fields_values", []) or []:
        if field.get("field_id") != settings.custom_field_id:
            continue
        values = field.get("values") or []
        if not values:
            return None
        raw = str(values[0].get("value", "")).strip()
        digits = "".join(ch for ch in raw if ch.isdigit())
        if not digits:
            return None
        return int(digits)
    return None


def is_target_stage(stage_id: int) -> bool:
    return stage_id in {settings.stage_2_4_id, settings.stage_6_9_id, settings.stage_12_plus_id}


def notify_invalid_quantity(lead_id: int, quantity: int | None, stage_id: int, reason: str) -> None:
    link = amo_client.lead_link(lead_id)
    send_telegram_message(
        f"⚠️ {reason}. Поле {settings.custom_field_id}: {quantity}. "
        f"Стадия: {stage_id}. Сделка: {link}"
    )


@app.post("/webhooks/amo")
async def amo_webhook(request: Request) -> JSONResponse:
    form = await request.form()
    form_data = {k: v for k, v in form.items()}
    status_updates = parse_status_updates(form_data)
    if not status_updates:
        return JSONResponse({"ok": True, "processed": 0})

    processed = 0
    with SessionLocal() as db:
        for item in status_updates:
            lead_id = item["lead_id"]
            stage_id = item["stage_id"]

            if not is_target_stage(stage_id):
                continue

            fingerprint_src = f"{lead_id}:{stage_id}:{item['updated_at']}"
            fingerprint = hashlib.sha256(fingerprint_src.encode()).hexdigest()
            hook = HookEvent(
                lead_id=lead_id,
                stage_id=stage_id,
                fingerprint=fingerprint,
                payload=form_data,
                processed=False,
            )
            db.add(hook)
            try:
                db.flush()
            except IntegrityError:
                db.rollback()
                continue

            try:
                lead = amo_client.get_lead(lead_id)
                quantity = extract_quantity(lead)
                allowed_for_stage = stage_allowed_quantities(
                    stage_id,
                    stage_2_4_id=settings.stage_2_4_id,
                    stage_6_9_id=settings.stage_6_9_id,
                    stage_12_plus_id=settings.stage_12_plus_id,
                )

                if quantity is None or quantity not in ALLOWED_QUANTITIES:
                    notify_invalid_quantity(lead_id, quantity, stage_id, "Неверное значение количества банок")
                    hook.processed = True
                    hook.error = f"invalid quantity: {quantity}"
                    db.add(hook)
                    processed += 1
                    continue

                if quantity not in allowed_for_stage:
                    notify_invalid_quantity(lead_id, quantity, stage_id, "Количество не соответствует стадии")
                    hook.processed = True
                    hook.error = f"quantity {quantity} does not match stage {stage_id}"
                    db.add(hook)
                    processed += 1
                    continue

                for due_at, text in build_due_timestamps(quantity, datetime.now(timezone.utc)):
                    amo_task_id = amo_client.create_task(lead_id=lead_id, text=text, complete_till=due_at)
                    db.add(
                        TaskRecord(
                            hook_id=hook.id,
                            lead_id=lead_id,
                            quantity=quantity,
                            due_at=due_at,
                            text=text,
                            amo_task_id=amo_task_id,
                        )
                    )

                hook.processed = True
                db.add(hook)
                processed += 1
            except Exception as exc:  # noqa: BLE001
                hook.error = str(exc)
                db.add(hook)

        db.commit()

    return JSONResponse({"ok": True, "processed": processed})
