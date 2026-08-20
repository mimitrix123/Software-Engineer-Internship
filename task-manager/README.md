# CLI Task Manager

A Python command-line task manager built with OOP principles. Tasks are persisted in a JSON file and support CRUD operations, priorities, due dates, completion state, input validation, and friendly error handling.

## Requirements

- Python 3.9+
- Optional development dependency: `pip install -r requirements-dev.txt`

## Usage

Run from the `task-manager` directory:

```bash
python -m task_manager.cli add "Finish assignment" -p high --due-date 2026-09-01
python -m task_manager.cli list
python -m task_manager.cli show 1
python -m task_manager.cli update 1 --completed
python -m task_manager.cli update 1 --priority medium --title "Finish project"
python -m task_manager.cli delete 1
```

Use `--file path/to/tasks.json` to choose a different JSON data file.

## Design

- `models.py` — `Task` domain object and validation.
- `storage.py` — JSON persistence through `JSONTaskRepository`.
- `service.py` — `TaskManager` business logic and CRUD operations.
- `cli.py` — argparse-based command-line interface and error handling.
- `tests/` — automated tests for CRUD, validation, corruption handling, and persistence.

## Testing

```bash
pytest -q
```

## Git history

The implementation is intentionally split into meaningful commits covering scaffolding, the domain model, persistence, service logic, CLI/error handling, tests, and development tooling.
