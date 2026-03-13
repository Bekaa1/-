from __future__ import annotations

from typing import Any

import httpx

from app.config import settings


class AmoClient:
    def __init__(self) -> None:
        self.base_url = f"https://{settings.amo_domain}.amocrm.ru"
        self.api_url = "https://api-b.amocrm.ru"
        self.headers = {
            "Authorization": f"Bearer {settings.amo_token}",
            "Content-Type": "application/json",
        }

    def get_lead(self, lead_id: int) -> dict[str, Any]:
        with httpx.Client(timeout=20) as client:
            response = client.get(
                f"{self.api_url}/api/v4/leads/{lead_id}",
                headers=self.headers,
                params={"with": "contacts,custom_fields_values"},
            )
            response.raise_for_status()
            return response.json()

    def create_task(self, lead_id: int, text: str, complete_till: int) -> int | None:
        payload = [{"entity_id": lead_id, "entity_type": "leads", "text": text, "complete_till": complete_till}]
        with httpx.Client(timeout=20) as client:
            response = client.post(f"{self.api_url}/api/v4/tasks", headers=self.headers, json=payload)
            response.raise_for_status()
            body = response.json()
            embedded = body.get("_embedded", {})
            tasks = embedded.get("tasks", [])
            if not tasks:
                return None
            return int(tasks[0]["id"])

    def lead_link(self, lead_id: int) -> str:
        return f"{self.base_url}/leads/detail/{lead_id}"
