from abc import ABC, abstractmethod

from spreadsheet.broker.event import Event


class Subscriber(ABC):
    pass


class Publisher(ABC):
    @abstractmethod
    def get_subs(self) -> list[Subscriber]:
        raise NotImplemented

    @abstractmethod
    def parse_events(self) -> list[Event]:
        raise NotImplemented


class Pubsub(Subscriber, Publisher, ABC):
    pass
