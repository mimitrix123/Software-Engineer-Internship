from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class LibraryEvent:
    action: str
    book_title: str
    message: str


class Observer(ABC):
    @abstractmethod
    def update(self, event: LibraryEvent) -> None:
        raise NotImplementedError


class ConsoleNotificationObserver(Observer):
    def update(self, event: LibraryEvent) -> None:
        print(f"[NOTIFICATION] {event.message}")


class EmailNotificationObserver(Observer):
    def __init__(self, recipient: str):
        self.recipient = recipient
        self.messages: list[str] = []

    def update(self, event: LibraryEvent) -> None:
        message = f"To: {self.recipient} | {event.message}"
        self.messages.append(message)


class NotificationSubject:
    def __init__(self) -> None:
        self._observers: list[Observer] = []

    def attach(self, observer: Observer) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, event: LibraryEvent) -> None:
        for observer in tuple(self._observers):
            observer.update(event)
