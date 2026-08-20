"""Tests for validation helpers."""

import unittest
from task_manager.validators import validate_due_date, validate_priority, validate_title


class ValidationTests(unittest.TestCase):
    def test_title_is_trimmed(self):
        self.assertEqual(validate_title("  task  "), "task")

    def test_empty_title_rejected(self):
        with self.assertRaises(ValueError):
            validate_title(" ")

    def test_priority_rejected(self):
        with self.assertRaises(ValueError):
            validate_priority("urgent")

    def test_due_date(self):
        self.assertEqual(validate_due_date("2026-12-31"), "2026-12-31")
        with self.assertRaises(ValueError):
            validate_due_date("2026-02-30")


if __name__ == "__main__":
    unittest.main()
