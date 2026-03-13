from datetime import datetime, timezone

from app.logic import PLANS_BY_QUANTITY, build_due_timestamps, stage_allowed_quantities


def test_task_count_matches_plan() -> None:
    base = datetime(2026, 1, 1, tzinfo=timezone.utc)
    for quantity, plan in PLANS_BY_QUANTITY.items():
        tasks = build_due_timestamps(quantity, base)
        assert len(tasks) == plan.total_tasks


def test_weekly_text_for_2_banks() -> None:
    base = datetime(2026, 1, 1, tzinfo=timezone.utc)
    tasks = build_due_timestamps(2, base)
    assert tasks[0][1] == "Прошла одна неделя, нужно позвонить"


def test_stage_to_quantity_mapping() -> None:
    assert stage_allowed_quantities(1, stage_2_4_id=1, stage_6_9_id=2, stage_12_plus_id=3) == {2, 4}
    assert stage_allowed_quantities(2, stage_2_4_id=1, stage_6_9_id=2, stage_12_plus_id=3) == {6, 9}
    assert stage_allowed_quantities(3, stage_2_4_id=1, stage_6_9_id=2, stage_12_plus_id=3) == {12, 15}
    assert stage_allowed_quantities(999, stage_2_4_id=1, stage_6_9_id=2, stage_12_plus_id=3) == set()
