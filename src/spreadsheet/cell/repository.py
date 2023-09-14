from abc import ABC, abstractmethod
from uuid import UUID

from loguru import logger

from spreadsheet.cell.entity import Cell


class CellRepo(ABC):
    @abstractmethod
    def add(self, cell: Cell):
        raise NotImplemented

    @abstractmethod
    def get_by_id(self, uuid: UUID) -> Cell:
        raise NotImplemented

    @abstractmethod
    def get_all(self) -> list[Cell]:
        raise NotImplemented

    @abstractmethod
    def get_filtred(self, filter_by: dict, order_by: dict, asc=True) -> list[Cell]:
        raise NotImplemented

    @abstractmethod
    def update(self, cell: Cell):
        raise NotImplemented


class CellRepoFake(CellRepo):
    def __init__(self):
        self._data: list[Cell] = []

    def add(self, cell: Cell):
        self._data.append(cell)

    def get_by_id(self, uuid: UUID) -> Cell:
        for cell in self._data:
            if cell.uuid == uuid:
                return cell
        raise LookupError

    def get_all(self) -> list[Cell]:
        return self._data

    def get_filtred(self, filter_by: dict, order_by: dict, asc=True) -> list[Cell]:
        result = []
        for cell in self._data:
            if all(cell.__getattribute__(key) == value for key, value in filter_by.items()):
                result.append(cell)
        if len(result) == 0:
            logger.warning(f"get_filtred => len(result) = 0")
        return result

    def update(self, data: Cell):
        for i, cell in enumerate(self._data):
            if cell.uuid == data.uuid:
                self._data[i] = data
                return
        raise LookupError
