from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class HookEvent(Base):
    __tablename__ = "hook_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    received_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    lead_id: Mapped[int | None] = mapped_column(Integer)
    stage_id: Mapped[int | None] = mapped_column(Integer)
    fingerprint: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    payload: Mapped[dict] = mapped_column(JSONB, nullable=False)
    processed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    error: Mapped[str | None] = mapped_column(Text)

    tasks: Mapped[list["TaskRecord"]] = relationship(back_populates="hook")


class TaskRecord(Base):
    __tablename__ = "task_records"
    __table_args__ = (UniqueConstraint("hook_id", "due_at", name="uq_task_per_due_date_per_hook"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    hook_id: Mapped[int] = mapped_column(ForeignKey("hook_events.id"), nullable=False)
    lead_id: Mapped[int] = mapped_column(Integer, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    due_at: Mapped[int] = mapped_column(Integer, nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    amo_task_id: Mapped[int | None] = mapped_column(Integer)

    hook: Mapped[HookEvent] = relationship(back_populates="tasks")
