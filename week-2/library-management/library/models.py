from dataclasses import dataclass


@dataclass
class Book:
    id: int
    title: str
    author: str
    isbn: str
    available: bool = True

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "available": self.available,
        }
