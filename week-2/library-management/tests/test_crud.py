import tempfile
import unittest
from pathlib import Path

from library.database import DatabaseConnection
from library.observer import EmailNotificationObserver, NotificationSubject
from library.repository import BookRepository
from library.service import LibraryService


class CrudTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        db = DatabaseConnection(Path(self.tmp.name) / "library.db")
        subject = NotificationSubject()
        self.observer = EmailNotificationObserver("test@example.com")
        subject.attach(self.observer)
        self.service = LibraryService(BookRepository(db), subject)
        self.db = db

    def tearDown(self):
        self.db.close()
        self.tmp.cleanup()

    def test_create_read_update_delete(self):
        book = self.service.create_book("Dune", "Frank Herbert", "9780441172719")
        self.assertEqual(self.service.get_book(book.id).title, "Dune")
        updated = self.service.update_book(book.id, "Dune Messiah", "Frank Herbert", "9780441294670", False)
        self.assertFalse(updated.available)
        self.assertEqual(len(self.service.list_books()), 1)
        self.service.delete_book(book.id)
        self.assertEqual(self.service.list_books(), [])
        self.assertEqual(len(self.observer.messages), 3)

    def test_missing_book_raises(self):
        with self.assertRaises(KeyError):
            self.service.get_book(999)

    def test_duplicate_isbn_rejected(self):
        self.service.create_book("Book A", "Author A", "ISBN-1")
        with self.assertRaises(Exception):
            self.service.create_book("Book B", "Author B", "ISBN-1")


if __name__ == "__main__":
    unittest.main()
