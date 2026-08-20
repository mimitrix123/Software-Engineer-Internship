from dataclasses import dataclass
from datetime import date
from typing import Optional


PRIORITIES = ("low", "medium", "high")


@dataclass
class Task:
    id: int
    title: str
    description: str
    priority: str
    due_date: Optional[str] = None
    completed: bool = False

    def validate(self) -> None:
        if not self.title.strip():
            raise ValueError("Title cannot be empty")
        if self.priority not in PRIORITIES:
            raise ValueError("Priority must be low, medium, or high")
        if self.due_date:
            try:
                date.fromisoformat(self.due_date)
            except ValueError as exc:
                raise ValueError("Due date must use YYYY-MM-DD format") from exc

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "due_date": self.due_date,
            "completed": self.completed,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        task = cls(
            id=int(data["id"]),
            title=str(data["title"]),
            description=str(data.get("description", "")),
            priority=str(data.get("priority", "medium")),
            due_date=data.get("due_date"),
            completed=bool(data.get("completed", False)),
        )
        task.validate()
        return task
