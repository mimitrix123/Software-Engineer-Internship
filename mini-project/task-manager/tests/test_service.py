"""Tests for service CRUD operations."""

import tempfile
import unittest
from pathlib import Path

from task_manager.repository import TaskRepository
from task_manager.service import TaskService


class ServiceTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.service = TaskService(TaskRepository(Path(self.tempdir.name) / "tasks.json"))

    def tearDown(self):
        self.tempdir.cleanup()

    def test_create_complete_update_delete(self):
        task = self.service.create("Ship feature", "high", "2026-12-31")
        self.assertEqual(task.id, 1)
        self.service.update(1, priority="low")
        self.assertEqual(self.service.get(1).priority, "low")
        self.service.complete(1)
        self.assertTrue(self.service.get(1).completed)
        self.service.delete(1)
        with self.assertRaises(KeyError):
            self.service.get(1)

    def test_unknown_task(self):
        with self.assertRaises(KeyError):
            self.service.get(99)


if __name__ == "__main__":
    unittest.main()
