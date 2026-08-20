"""Input validation for task fields."""

from datetime import date

VALID_PRIORITIES = {"low", "medium", "high"}


def validate_title(title: str) -> str:
    value = title.strip()
    if not value:
        raise ValueError("Title cannot be empty.")
    if len(value) > 200:
        raise ValueError("Title must be 200 characters or fewer.")
    return value


def validate_priority(priority: str) -> str:
    value = priority.strip().lower()
    if value not in VALID_PRIORITIES:
        raise ValueError("Priority must be low, medium, or high.")
    return value


def validate_due_date(due_date: str | None) -> str | None:
    if due_date is None or not due_date.strip():
        return None
    value = due_date.strip()
    try:
        date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError("Due date must be a valid date in YYYY-MM-DD format.") from exc
    return value
