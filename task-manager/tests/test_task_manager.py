import json

import pytest

from task_manager.models import Task
from task_manager.service import TaskManager
from task_manager.storage import JSONTaskRepository


def manager(tmp_path):
    return TaskManager(JSONTaskRepository(str(tmp_path / "tasks.json")))


def test_create_and_list(tmp_path):
    service = manager(tmp_path)
    created = service.create("Ship feature", "write docs", "high", "2026-09-01")
    assert created.id == 1
    assert service.list_tasks()[0].title == "Ship feature"


def test_update_and_delete(tmp_path):
    service = manager(tmp_path)
    task = service.create("Old", "", "low", None)
    updated = service.update(task.id, title="New", completed=True)
    assert updated.title == "New"
    assert updated.completed is True
    service.delete(task.id)
    assert service.list_tasks() == []


def test_validation_rejects_bad_date(tmp_path):
    with pytest.raises(ValueError, match="YYYY-MM-DD"):
        manager(tmp_path).create("Task", "", "medium", "tomorrow")


def test_corrupt_json_is_reported(tmp_path):
    path = tmp_path / "tasks.json"
    path.write_text("{broken", encoding="utf-8")
    with pytest.raises(ValueError, match="Invalid JSON"):
        JSONTaskRepository(str(path)).load()


def test_json_round_trip(tmp_path):
    path = tmp_path / "tasks.json"
    repository = JSONTaskRepository(str(path))
    task = Task(1, "Test", "Description", "medium", "2026-10-01")
    repository.save([task])
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data[0]["title"] == "Test"
    assert repository.load()[0] == task
