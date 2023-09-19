from abc import ABC, abstractmethod

from spreadsheet.abstract.pydantic_model import PydanticModel
from spreadsheet.abstract.event import Event


class Subscriber(ABC):
    @abstractmethod
    def on_before_start(self):
        raise NotImplemented

    @abstractmethod
    def on_subscribe(self, data: PydanticModel):
        raise NotImplemented

    @abstractmethod
    def on_complete(self):
        raise NotImplemented


class Publisher(ABC):
    @abstractmethod
    def subscribe(self, subs: list[Subscriber]):
        raise NotImplemented

    @abstractmethod
    def get_subs(self) -> list[Subscriber]:
        raise NotImplemented

    @abstractmethod
    def parse_events(self) -> list[Event]:
        raise NotImplemented


class Pubsub(Subscriber, Publisher, ABC):
    pass
