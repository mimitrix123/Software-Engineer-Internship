"""Application service containing task CRUD use-cases."""

from .models import Task
from .repository import TaskRepository
from .validators import validate_due_date, validate_priority, validate_title


class TaskService:
    def __init__(self, repository: TaskRepository) -> None:
        self.repository = repository

    def create(self, title: str, priority: str = "medium", due_date: str | None = None) -> Task:
        tasks = self.repository.list()
        task_id = max((task.id for task in tasks), default=0) + 1
        task = Task(task_id, validate_title(title), validate_priority(priority), validate_due_date(due_date))
        return self.repository.add(task)

    def list_tasks(self) -> list[Task]:
        return self.repository.list()

    def get(self, task_id: int) -> Task:
        task = self.repository.get(task_id)
        if task is None:
            raise KeyError(f"Task #{task_id} not found.")
        return task

    def update(self, task_id: int, title: str | None = None, priority: str | None = None, due_date: str | None = None) -> Task:
        task = self.get(task_id)
        if title is not None:
            task.title = validate_title(title)
        if priority is not None:
            task.priority = validate_priority(priority)
        if due_date is not None:
            task.due_date = validate_due_date(due_date)
        return self.repository.update(task)

    def complete(self, task_id: int) -> Task:
        task = self.get(task_id)
        task.completed = True
        return self.repository.update(task)

    def delete(self, task_id: int) -> None:
        self.repository.delete(task_id)
