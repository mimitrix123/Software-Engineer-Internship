"""Task domain model."""

from dataclasses import asdict, dataclass
from datetime import date
from typing import Any


@dataclass
class Task:
    id: int
    title: str
    priority: str = "medium"
    due_date: str | None = None
    completed: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Task":
        return cls(
            id=int(data["id"]),
            title=str(data["title"]),
            priority=str(data.get("priority", "medium")),
            due_date=data.get("due_date"),
            completed=bool(data.get("completed", False)),
        )

    @property
    def is_overdue(self) -> bool:
        return bool(self.due_date and not self.completed and date.fromisoformat(self.due_date) < date.today())
