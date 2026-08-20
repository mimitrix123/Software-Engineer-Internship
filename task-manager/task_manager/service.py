from typing import List, Optional

from .models import PRIORITIES, Task
from .storage import JSONTaskRepository


class TaskManager:
    def __init__(self, repository: JSONTaskRepository) -> None:
        self.repository = repository

    def list_tasks(self) -> List[Task]:
        return sorted(self.repository.load(), key=lambda t: (t.completed, t.due_date or "9999-12-31", t.id))

    def create(self, title: str, description: str, priority: str, due_date: Optional[str]) -> Task:
        tasks = self.repository.load()
        next_id = max((task.id for task in tasks), default=0) + 1
        task = Task(next_id, title.strip(), description.strip(), priority, due_date)
        task.validate()
        tasks.append(task)
        self.repository.save(tasks)
        return task

    def get(self, task_id: int) -> Task:
        for task in self.repository.load():
            if task.id == task_id:
                return task
        raise LookupError(f"Task {task_id} not found")

    def update(self, task_id: int, **changes) -> Task:
        tasks = self.repository.load()
        task = next((item for item in tasks if item.id == task_id), None)
        if task is None:
            raise LookupError(f"Task {task_id} not found")
        for field, value in changes.items():
            if value is not None and hasattr(task, field):
                setattr(task, field, value.strip() if isinstance(value, str) else value)
        task.validate()
        self.repository.save(tasks)
        return task

    def delete(self, task_id: int) -> None:
        tasks = self.repository.load()
        remaining = [task for task in tasks if task.id != task_id]
        if len(remaining) == len(tasks):
            raise LookupError(f"Task {task_id} not found")
        self.repository.save(remaining)
