# CLI Task Manager

A dependency-free Python command-line task manager using OOP and JSON persistence.

## Features
- Create, read/list, update, complete, and delete tasks
- Priority levels: low, medium, high
- Optional due dates in `YYYY-MM-DD` format
- Input validation with clear error messages
- Graceful handling of missing/corrupt JSON data
- Atomic JSON writes to reduce the chance of partial data files
- Unit tests for validation, persistence, CRUD, and CLI behavior

## Project structure
```text
mini-project/task-manager/
├── task_manager/
│   ├── __init__.py
│   ├── cli.py
│   ├── models.py
│   ├── repository.py
│   ├── service.py
│   └── validators.py
├── tests/
│   ├── test_repository.py
│   ├── test_service.py
│   └── test_validators.py
├── data/
│   └── tasks.json
├── main.py
├── requirements.txt
└── README.md
```

## Requirements
- Python 3.10+
- No third-party runtime dependencies

## Run
From this directory:

```bash
python main.py
```

Or:

```bash
python -m task_manager.cli
```

## Commands
The interactive menu supports:

1. Create task
2. List tasks
3. View task
4. Update task
5. Mark task complete
6. Delete task
7. Exit

### Validation
- Title cannot be empty.
- Priority must be `low`, `medium`, or `high`.
- Due dates must use `YYYY-MM-DD` and must be valid calendar dates.
- Task IDs must refer to an existing task.

## Example
```text
$ python main.py

=== Task Manager ===
1. Create task
2. List tasks
3. View task
4. Update task
5. Mark task complete
6. Delete task
7. Exit
Choose an option: 1
Title: Finish internship project
Priority (low/medium/high): high
Due date (YYYY-MM-DD, blank for none): 2026-08-31
Created task #1.
```

## Testing
```bash
python -m unittest discover -s tests -v
```
