from abc import ABC, abstractmethod

from loguru import logger

from .entity import Formula


class FormulaRepo(ABC):
    @abstractmethod
    def add(self, entity: Formula):
        raise NotImplemented

    @abstractmethod
    def get_all(self) -> list[Formula]:
        raise NotImplemented

    @abstractmethod
    def update(self, entity: Formula):
        raise NotImplemented


class FormulaRepoFake(FormulaRepo):
    def __init__(self):
        self._data: list[Formula] = []

    def add(self, entity: Formula):
        self._data.append(entity)

    def get_all(self) -> list[Formula]:
        return self._data

    def update(self, entity: Formula):
        for i, item in enumerate(self._data):
            if item.uuid == entity.uuid:
                self._data[i] = entity
                return
        raise LookupError
