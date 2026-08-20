import argparse
from typing import Optional

from .models import PRIORITIES
from .service import TaskManager
from .storage import JSONTaskRepository


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Command-line task manager")
    parser.add_argument("--file", default="tasks.json", help="JSON data file")
    sub = parser.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add", help="Create a task")
    add.add_argument("title")
    add.add_argument("-d", "--description", default="")
    add.add_argument("-p", "--priority", choices=PRIORITIES, default="medium")
    add.add_argument("--due-date")

    sub.add_parser("list", help="List tasks")
    show = sub.add_parser("show", help="Show a task")
    show.add_argument("id", type=int)

    update = sub.add_parser("update", help="Update a task")
    update.add_argument("id", type=int)
    update.add_argument("--title")
    update.add_argument("-d", "--description")
    update.add_argument("-p", "--priority", choices=PRIORITIES)
    update.add_argument("--due-date")
    update.add_argument("--completed", action="store_true")
    update.add_argument("--incomplete", action="store_true")

    delete = sub.add_parser("delete", help="Delete a task")
    delete.add_argument("id", type=int)
    return parser


def print_task(task) -> None:
    status = "done" if task.completed else "open"
    due = task.due_date or "none"
    print(f"#{task.id} [{status}] {task.title} | priority={task.priority} | due={due}")
    if task.description:
        print(f"  {task.description}")


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    manager = TaskManager(JSONTaskRepository(args.file))
    try:
        if args.command == "add":
            task = manager.create(args.title, args.description, args.priority, args.due_date)
            print(f"Created task {task.id}")
        elif args.command == "list":
            tasks = manager.list_tasks()
            if not tasks:
                print("No tasks found.")
            for task in tasks:
                print_task(task)
        elif args.command == "show":
            print_task(manager.get(args.id))
        elif args.command == "update":
            if args.completed and args.incomplete:
                parser.error("--completed and --incomplete cannot be used together")
            changes = {"title": args.title, "description": args.description, "priority": args.priority, "due_date": args.due_date}
            if args.completed:
                changes["completed"] = True
            elif args.incomplete:
                changes["completed"] = False
            task = manager.update(args.id, **changes)
            print(f"Updated task {task.id}")
        elif args.command == "delete":
            manager.delete(args.id)
            print(f"Deleted task {args.id}")
        return 0
    except (ValueError, LookupError, OSError) as exc:
        print(f"Error: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
