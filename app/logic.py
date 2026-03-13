from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone


@dataclass(frozen=True)
class TaskPlan:
    total_tasks: int
    step_days: int
    months: int
    text: str


TASK_TEXT_WEEKLY = "Прошла одна неделя, нужно позвонить"
TASK_TEXT_BIWEEKLY = "Прошло две недели, нужно позвонить"

ALLOWED_QUANTITIES = {2, 4, 6, 9, 12, 15}

PLANS_BY_QUANTITY: dict[int, TaskPlan] = {
    2: TaskPlan(total_tasks=8, step_days=7, months=2, text=TASK_TEXT_WEEKLY),
    4: TaskPlan(total_tasks=8, step_days=14, months=4, text=TASK_TEXT_BIWEEKLY),
    6: TaskPlan(total_tasks=12, step_days=14, months=6, text=TASK_TEXT_BIWEEKLY),
    9: TaskPlan(total_tasks=18, step_days=14, months=9, text=TASK_TEXT_BIWEEKLY),
    12: TaskPlan(total_tasks=24, step_days=14, months=12, text=TASK_TEXT_BIWEEKLY),
    15: TaskPlan(total_tasks=30, step_days=14, months=15, text=TASK_TEXT_BIWEEKLY),
}


def stage_allowed_quantities(stage_id: int, *, stage_2_4_id: int, stage_6_9_id: int, stage_12_plus_id: int) -> set[int]:
    if stage_id == stage_2_4_id:
        return {2, 4}
    if stage_id == stage_6_9_id:
        return {6, 9}
    if stage_id == stage_12_plus_id:
        return {12, 15}
    return set()


def build_due_timestamps(quantity: int, start_at: datetime | None = None) -> list[tuple[int, str]]:
    plan = PLANS_BY_QUANTITY[quantity]
    base = start_at or datetime.now(timezone.utc)
    schedule: list[tuple[int, str]] = []
    for i in range(1, plan.total_tasks + 1):
        due_dt = base + timedelta(days=plan.step_days * i)
        schedule.append((int(due_dt.timestamp()), plan.text))
    return schedule
