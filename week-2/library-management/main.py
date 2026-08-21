from pathlib import Path

from library.database import DatabaseConnection
from library.observer import ConsoleNotificationObserver, EmailNotificationObserver, NotificationSubject
from library.repository import BookRepository
from library.service import LibraryService


def main() -> None:
    database = DatabaseConnection(Path(__file__).with_name("library.db"))
    subject = NotificationSubject()
    subject.attach(ConsoleNotificationObserver())
    subject.attach(EmailNotificationObserver("librarian@example.com"))
    service = LibraryService(BookRepository(database), subject)

    while True:
        print("\n=== Library Management System ===")
        print("1. Add book\n2. List books\n3. View book\n4. Update book\n5. Delete book\n6. Exit")
        choice = input("Choose an option: ").strip()
        try:
            if choice == "1":
                book = service.create_book(input("Title: "), input("Author: "), input("ISBN: "))
                print(f"Created book #{book.id}.")
            elif choice == "2":
                books = service.list_books()
                if not books:
                    print("No books found.")
                for book in books:
                    print(f"#{book.id} | {book.title} | {book.author} | ISBN: {book.isbn} | {'Available' if book.available else 'Unavailable'}")
            elif choice == "3":
                book = service.get_book(int(input("Book ID: ")))
                print(book)
            elif choice == "4":
                book_id = int(input("Book ID: "))
                current = service.get_book(book_id)
                title = input(f"Title [{current.title}]: ").strip() or current.title
                author = input(f"Author [{current.author}]: ").strip() or current.author
                isbn = input(f"ISBN [{current.isbn}]: ").strip() or current.isbn
                available = input(f"Available [{current.available}] (y/n): ").strip().lower() != "n"
                service.update_book(book_id, title, author, isbn, available)
                print("Book updated.")
            elif choice == "5":
                book_id = int(input("Book ID: "))
                service.delete_book(book_id)
                print("Book deleted.")
            elif choice == "6":
                break
            else:
                print("Invalid option. Choose 1-6.")
        except (ValueError, KeyError) as exc:
            print(f"Error: {exc}")
        except Exception as exc:
            print(f"Database error: {exc}")
    database.close()


if __name__ == "__main__":
    main()
