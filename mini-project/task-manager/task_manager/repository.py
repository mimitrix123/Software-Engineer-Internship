"""JSON persistence layer."""

import json
import os
import tempfile
from pathlib import Path

from .models import Task


class TaskRepository:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self._write([])

    def _read(self) -> list[Task]:
        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
            if not isinstance(raw, list):
                raise ValueError("Task data must be a JSON list.")
            return [Task.from_dict(item) for item in raw]
        except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
            raise RuntimeError(f"Unable to read task data: {exc}") from exc

    def _write(self, tasks: list[Task | dict]) -> None:
        payload = [task.to_dict() if isinstance(task, Task) else task for task in tasks]
        fd, temp_name = tempfile.mkstemp(dir=self.path.parent, prefix=".tasks-", suffix=".tmp", text=True)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                json.dump(payload, handle, indent=2)
                handle.write("\n")
            os.replace(temp_name, self.path)
        except OSError as exc:
            try:
                os.unlink(temp_name)
            except OSError:
                pass
            raise RuntimeError(f"Unable to save task data: {exc}") from exc

    def list(self) -> list[Task]:
        return self._read()

    def get(self, task_id: int) -> Task | None:
        return next((task for task in self._read() if task.id == task_id), None)

    def add(self, task: Task) -> Task:
        tasks = self._read()
        tasks.append(task)
        self._write(tasks)
        return task

    def update(self, task: Task) -> Task:
        tasks = self._read()
        for index, existing in enumerate(tasks):
            if existing.id == task.id:
                tasks[index] = task
                self._write(tasks)
                return task
        raise KeyError(f"Task #{task.id} not found.")

    def delete(self, task_id: int) -> None:
        tasks = self._read()
        remaining = [task for task in tasks if task.id != task_id]
        if len(remaining) == len(tasks):
            raise KeyError(f"Task #{task_id} not found.")
        self._write(remaining)
