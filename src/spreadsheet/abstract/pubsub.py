from abc import ABC, abstractmethod
from typing import Union

from spreadsheet.abstract.cell_value import CellTable


class Subscriber(ABC):
    @abstractmethod
    def on_before_start(self):
        raise NotImplemented

    @abstractmethod
    def on_subscribe(self, data: CellTable):
        raise NotImplemented

    @abstractmethod
    def on_update(self, old_data: CellTable, new_data: CellTable):
        raise NotImplemented

    @abstractmethod
    def on_complete(self):
        raise NotImplemented


class Publisher(ABC):
    @abstractmethod
    def get_entity(self):
        raise NotImplemented

    @abstractmethod
    def notify(self):
        raise NotImplemented

    @abstractmethod
    def subscribe(self, subs: Union['Pubsub', list['Pubsub']]):
        raise NotImplemented


class Pubsub(Publisher, Subscriber, ABC):
    pass
