from abc import ABC, abstractmethod

from spreadsheet.abstract.event import Event


class Handler(ABC):
    @abstractmethod
    def handle(self):
        pass

    @abstractmethod
    def parse_new_events(self) -> list[Event]:
        raise NotImplemented
    