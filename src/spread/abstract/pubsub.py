from abc import ABC, abstractmethod
from uuid import UUID, uuid4

from spread.abstract.event import Event
from spread.abstract.pydantic_model import PydanticModel


class Subscriber(ABC):
    def __init__(self, uuid: UUID | None):
        self.uuid = uuid if uuid is not None else uuid4()
        self._events = set()

    @abstractmethod
    def on_before_start(self):
        raise NotImplemented

    @abstractmethod
    def on_unsubscribe(self):
        raise NotImplemented

    @abstractmethod
    def on_subscribe(self, data: PydanticModel):
        raise NotImplemented

    @abstractmethod
    def on_update(self, old_data: PydanticModel, new_data: PydanticModel):
        raise NotImplemented

    @abstractmethod
    def on_complete(self):
        raise NotImplemented

    def parse_events(self) -> set[Event]:
        events = self._events
        self._events = set()
        return events


class Publisher(ABC):
    @abstractmethod
    def notify(self):
        raise NotImplemented

    @abstractmethod
    def subscribe(self, subs: set[Subscriber]):
        raise NotImplemented

    @abstractmethod
    def unsubscribe(self, subs: set[Subscriber]):
        raise NotImplemented


class Pubsub(Subscriber, Publisher, ABC):
    pass
