from abc import ABC, abstractmethod
from uuid import UUID

from .entity import Sheet


class SheetRepo(ABC):
    @abstractmethod
    def add(self, sheet: Sheet):
        raise NotImplemented

    @abstractmethod
    def get_all(self) -> list[Sheet]:
        raise NotImplemented

    @abstractmethod
    def get_by_id(self, uuid: UUID) -> Sheet:
        raise NotImplemented

    @abstractmethod
    def update(self, sheet: Sheet):
        raise NotImplemented


class SheetRepoFake(SheetRepo):
    def __init__(self):
        self._data: list[Sheet] = []

    def add(self, sheet: Sheet):
        self._data.append(sheet)

    def get_all(self) -> list[Sheet]:
        return self._data

    def get_by_id(self, uuid: UUID) -> Sheet:
        for sheet in self._data:
            if sheet.uuid == uuid:
                return sheet
        raise LookupError

    def update(self, data: Sheet):
        for i, sheet in enumerate(self._data):
            if sheet.uuid == data.uuid:
                self._data[i] = data
                return 
        raise LookupError
