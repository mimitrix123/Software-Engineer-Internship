from .models import Book


class BookFactory:
    """Factory responsible for constructing Book objects."""

    @staticmethod
    def create_book(book_id: int, title: str, author: str, isbn: str, available: bool = True) -> Book:
        title = title.strip()
        author = author.strip()
        isbn = isbn.strip()
        if not title:
            raise ValueError("Book title cannot be empty.")
        if not author:
            raise ValueError("Author cannot be empty.")
        if not isbn:
            raise ValueError("ISBN cannot be empty.")
        return Book(book_id, title, author, isbn, available)
