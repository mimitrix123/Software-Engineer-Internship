from .factory import BookFactory
from .models import Book
from .observer import LibraryEvent, NotificationSubject
from .repository import BookRepository


class LibraryService:
    def __init__(self, repository: BookRepository, notifications: NotificationSubject | None = None):
        self.repository = repository
        self.notifications = notifications or NotificationSubject()

    def create_book(self, title: str, author: str, isbn: str) -> Book:
        books = self.repository.list_all()
        book = BookFactory.create_book(max((b.id for b in books), default=0) + 1, title, author, isbn)
        created = self.repository.create(book)
        self.notifications.notify(LibraryEvent("created", book.title, f"Book created: {book.title}"))
        return created

    def list_books(self) -> list[Book]:
        return self.repository.list_all()

    def get_book(self, book_id: int) -> Book:
        book = self.repository.get(book_id)
        if book is None:
            raise KeyError(f"Book #{book_id} not found.")
        return book

    def update_book(self, book_id: int, title: str, author: str, isbn: str, available: bool) -> Book:
        current = self.get_book(book_id)
        book = BookFactory.create_book(book_id, title, author, isbn, available)
        updated = self.repository.update(book)
        self.notifications.notify(LibraryEvent("updated", book.title, f"Book updated: {current.title} -> {book.title}"))
        return updated

    def delete_book(self, book_id: int) -> None:
        book = self.get_book(book_id)
        self.repository.delete(book_id)
        self.notifications.notify(LibraryEvent("deleted", book.title, f"Book deleted: {book.title}"))
