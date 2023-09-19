from abc import ABC, abstractmethod

from spread.abstract.pydantic_model import PydanticModel


class Subscriber(ABC):
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


class Publisher(ABC):
    @abstractmethod
    def notify(self):
        raise NotImplemented

    @abstractmethod
    def subscribe(self, subs: list[Subscriber]):
        raise NotImplemented

    @abstractmethod
    def unsubscribe(self, subs: list[Subscriber]):
        raise NotImplemented


class Pubsub(Subscriber, Publisher, ABC):
    pass
