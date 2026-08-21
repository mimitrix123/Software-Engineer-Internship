import tempfile
import unittest
from pathlib import Path

from library.database import DatabaseConnection
from library.factory import BookFactory
from library.observer import EmailNotificationObserver, LibraryEvent, NotificationSubject


class PatternTests(unittest.TestCase):
    def test_factory_creates_valid_book(self):
        book = BookFactory.create_book(1, " Clean Code ", "Robert Martin", "9780132350884")
        self.assertEqual(book.title, "Clean Code")
        self.assertTrue(book.available)

    def test_factory_rejects_empty_title(self):
        with self.assertRaises(ValueError):
            BookFactory.create_book(1, "", "Author", "ISBN")

    def test_observer_receives_events(self):
        subject = NotificationSubject()
        observer = EmailNotificationObserver("test@example.com")
        subject.attach(observer)
        subject.notify(LibraryEvent("created", "Book", "Book created: Book"))
        self.assertEqual(len(observer.messages), 1)
        self.assertIn("test@example.com", observer.messages[0])

    def test_observer_can_detach(self):
        subject = NotificationSubject()
        observer = EmailNotificationObserver("test@example.com")
        subject.attach(observer)
        subject.detach(observer)
        subject.notify(LibraryEvent("created", "Book", "Book created: Book"))
        self.assertEqual(observer.messages, [])

    def test_database_is_singleton(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "library.db"
            first = DatabaseConnection(path)
            second = DatabaseConnection(path)
            self.assertIs(first, second)
            first.close()


if __name__ == "__main__":
    unittest.main()
