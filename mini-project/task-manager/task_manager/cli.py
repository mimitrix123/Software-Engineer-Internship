"""Interactive command-line interface."""

from pathlib import Path

from .repository import TaskRepository
from .service import TaskService

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "tasks.json"


def _print_task(task) -> None:
    status = "done" if task.completed else ("overdue" if task.is_overdue else "open")
    due = task.due_date or "-"
    print(f"#{task.id:<3} {task.title:<35} priority={task.priority:<6} due={due:<10} status={status}")


def _ask_int(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("Please enter a valid task ID number.")


def _ask_required(prompt: str) -> str:
    while True:
        value = input(prompt)
        if value.strip():
            return value
        print("This value cannot be empty.")


def _ask_optional(prompt: str) -> str | None:
    value = input(prompt).strip()
    return value or None


def _create(service: TaskService) -> None:
    try:
        task = service.create(
            _ask_required("Title: "),
            input("Priority (low/medium/high) [medium]: ").strip() or "medium",
            _ask_optional("Due date (YYYY-MM-DD, blank for none): "),
        )
        print(f"Created task #{task.id}.")
    except (ValueError, RuntimeError) as exc:
        print(f"Error: {exc}")


def _list(service: TaskService) -> None:
    tasks = service.list_tasks()
    if not tasks:
        print("No tasks found.")
        return
    for task in sorted(tasks, key=lambda item: item.id):
        _print_task(task)


def _view(service: TaskService) -> None:
    try:
        _print_task(service.get(_ask_int("Task ID: ")))
    except (KeyError, RuntimeError) as exc:
        print(f"Error: {exc}")


def _update(service: TaskService) -> None:
    task_id = _ask_int("Task ID: ")
    try:
        task = service.get(task_id)
        print("Press Enter to keep the current value.")
        title = input(f"Title [{task.title}]: ").strip() or task.title
        priority = input(f"Priority [{task.priority}]: ").strip() or task.priority
        due = input(f"Due date [{task.due_date or '-'}] (use '-' to clear): ").strip()
        due_date = None if due == "-" else (due or task.due_date)
        service.update(task_id, title, priority, due_date)
        print(f"Updated task #{task_id}.")
    except (KeyError, ValueError, RuntimeError) as exc:
        print(f"Error: {exc}")


def run() -> None:
    service = TaskService(TaskRepository(DATA_FILE))
    actions = {
        "1": lambda: _create(service),
        "2": lambda: _list(service),
        "3": lambda: _view(service),
        "4": lambda: _update(service),
        "5": lambda: _complete(service),
        "6": lambda: _delete(service),
    }
    while True:
        print("\n=== Task Manager ===")
        print("1. Create task\n2. List tasks\n3. View task\n4. Update task\n5. Mark task complete\n6. Delete task\n7. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "7":
            print("Goodbye!")
            break
        action = actions.get(choice)
        if action:
            action()
        else:
            print("Invalid option. Choose 1-7.")


def _complete(service: TaskService) -> None:
    try:
        task = service.complete(_ask_int("Task ID: "))
        print(f"Completed task #{task.id}.")
    except (KeyError, RuntimeError) as exc:
        print(f"Error: {exc}")


def _delete(service: TaskService) -> None:
    try:
        task_id = _ask_int("Task ID: ")
        service.delete(task_id)
        print(f"Deleted task #{task_id}.")
    except (KeyError, RuntimeError) as exc:
        print(f"Error: {exc}")


if __name__ == "__main__":
    run()
