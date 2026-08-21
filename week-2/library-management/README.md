# Week 2 — Library Management System

A Python CLI library management system demonstrating three classic design patterns:

- **Factory Pattern** — creates `Book` domain objects without coupling callers to concrete construction.
- **Observer Pattern** — publishes book events to notification observers.
- **Singleton Pattern** — provides one shared database connection instance.

## Features
- Book CRUD: create, list, get, update, delete
- SQLite persistence through a Singleton database connection
- Email-style and console notification observers
- Input validation and error handling
- Interactive CLI
- Comprehensive unit tests using Python's standard `unittest` framework

## Run
```bash
cd week-2/library-management
python main.py
```

## Test
```bash
python -m unittest discover -s tests -v
```

No third-party runtime dependencies are required. Python 3.10+ is recommended.
