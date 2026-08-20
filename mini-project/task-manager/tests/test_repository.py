"""Tests for the JSON repository."""

import json
import tempfile
import unittest
from pathlib import Path

from task_manager.models import Task
from task_manager.repository import TaskRepository


class RepositoryTests(unittest.TestCase):
    def test_add_get_update_delete_persists(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tasks.json"
            repository = TaskRepository(path)
            task = repository.add(Task(1, "Write tests", "high", "2026-12-31"))
            self.assertEqual(repository.get(1).title, "Write tests")
            task.title = "Write better tests"
            repository.update(task)
            self.assertEqual(repository.get(1).title, "Write better tests")
            self.assertEqual(json.loads(path.read_text()), [task.to_dict()])
            repository.delete(1)
            self.assertIsNone(repository.get(1))

    def test_missing_file_is_created(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "nested" / "tasks.json"
            TaskRepository(path)
            self.assertTrue(path.exists())


if __name__ == "__main__":
    unittest.main()
