from .database import DatabaseConnection
from .factory import BookFactory
from .models import Book


class BookRepository:
    def __init__(self, database: DatabaseConnection):
        self.database = database

    def create(self, book: Book) -> Book:
        self.database.execute(
            "INSERT INTO books (id, title, author, isbn, available) VALUES (?, ?, ?, ?, ?)",
            (book.id, book.title, book.author, book.isbn, int(book.available)),
        )
        return book

    def list_all(self) -> list[Book]:
        rows = self.database.execute("SELECT * FROM books ORDER BY id").fetchall()
        return [self._from_row(row) for row in rows]

    def get(self, book_id: int) -> Book | None:
        row = self.database.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()
        return self._from_row(row) if row else None

    def update(self, book: Book) -> Book:
        cursor = self.database.execute(
            "UPDATE books SET title = ?, author = ?, isbn = ?, available = ? WHERE id = ?",
            (book.title, book.author, book.isbn, int(book.available), book.id),
        )
        if cursor.rowcount == 0:
            raise KeyError(f"Book #{book.id} not found.")
        return book

    def delete(self, book_id: int) -> None:
        cursor = self.database.execute("DELETE FROM books WHERE id = ?", (book_id,))
        if cursor.rowcount == 0:
            raise KeyError(f"Book #{book_id} not found.")

    @staticmethod
    def _from_row(row) -> Book:
        return BookFactory.create_book(row["id"], row["title"], row["author"], row["isbn"], bool(row["available"]))
