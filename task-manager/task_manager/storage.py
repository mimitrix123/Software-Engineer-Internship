import json
from pathlib import Path
from typing import List

from .models import Task


class JSONTaskRepository:
    def __init__(self, path: str = "tasks.json") -> None:
        self.path = Path(path)

    def load(self) -> List[Task]:
        if not self.path.exists():
            return []
        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
            if not isinstance(raw, list):
                raise ValueError("Task data must be a JSON list")
            return [Task.from_dict(item) for item in raw]
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON in {self.path}") from exc
        except (KeyError, TypeError) as exc:
            raise ValueError(f"Invalid task data in {self.path}") from exc

    def save(self, tasks: List[Task]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = [task.to_dict() for task in tasks]
        temp_path = self.path.with_suffix(self.path.suffix + ".tmp")
        temp_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        temp_path.replace(self.path)
