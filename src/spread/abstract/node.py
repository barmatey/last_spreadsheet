import typing
from abc import ABC, abstractmethod
from uuid import UUID, uuid4

from spread.abstract.pydantic_model import PydanticModel


class MessageBus(ABC):
    pass


class Node(ABC):
    def __init__(
            self,
            value: PydanticModel,
            messagebus: MessageBus,
            subs: set['Node'] = None,
            uuid: UUID = None
    ):
        self._value = value
        self._old_value = None
        self._messagebus = messagebus
        self._subs: set['Node'] = subs if subs is not None else set()
        self.uuid = uuid if uuid is not None else uuid4()

    def append_subscribers(self, subs: set['Node']):
        for sub in subs:
            sub.on_before_start()
            sub.on_subscribe(self._value)
            sub.on_complete()
            self._subs.add(sub)

    def remove_subscribers(self, subs: set['Node']):
        for sub in subs:
            sub.on_before_start()
            sub.on_unsubscribe(self._value)
            sub.on_complete()

    def notify(self):
        for sub in self._subs:
            sub.on_before_start()
            sub.on_update(self._old_value, self._value)
            sub.on_complete()

    def on_before_start(self):
        self._old_value = self._value.model_copy(deep=True)

    @abstractmethod
    def on_subscribe(self, data: PydanticModel):
        raise NotImplemented

    @abstractmethod
    def on_update(self, old_data: PydanticModel, new_data: PydanticModel):
        raise NotImplemented

    @abstractmethod
    def on_unsubscribe(self, data: PydanticModel):
        raise NotImplemented

    @abstractmethod
    def on_complete(self):
        raise NotImplemented
