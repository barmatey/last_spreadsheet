from abc import ABC, abstractmethod
from uuid import UUID

from loguru import logger

from spreadsheet.abstract.cell_value import CellValue
from spreadsheet.cell.entity import Cell


class CellRepo(ABC):
    @abstractmethod
    def add(self, cell: Cell):
        raise NotImplemented

    @abstractmethod
    def get_all(self) -> list[Cell]:
        raise NotImplemented

    @abstractmethod
    def get_by_id(self, uuid: UUID) -> Cell:
        raise NotImplemented

    @abstractmethod
    def get_by_index(self, sheet_id: UUID, index: tuple[int, int]) -> Cell:
        raise NotImplemented

    @abstractmethod
    def get_by_index_or_create(self, sheet_id: UUID, index: tuple[int, int]) -> Cell:
        raise NotImplemented

    @abstractmethod
    def get_filtred(self, filter_by: dict, order_by: list[str] = None, asc=True) -> list[Cell]:
        raise NotImplemented

    @abstractmethod
    def get_filtred_as_cell_values_table(self, columns: int, filter_by: dict, order_by: list[str] = None,
                                         asc=True) -> list[list[CellValue]]:
        raise NotImplemented

    @abstractmethod
    def update(self, cell: Cell):
        raise NotImplemented


class CellRepoFake(CellRepo):
    def __init__(self):
        self._data: list[Cell] = []

    def add(self, cell: Cell):
        self._data.append(cell)

    def get_all(self) -> list[Cell]:
        return self._data

    def get_by_id(self, uuid: UUID) -> Cell:
        for cell in self._data:
            if cell.uuid == uuid:
                return cell
        raise LookupError

    def get_by_index(self, sheet_id: UUID, index: tuple[int, int]) -> Cell:
        for cell in self._data:
            if cell.sheet_id == sheet_id and cell.index == index:
                return cell
        raise LookupError(f"index={index}")

    def get_by_index_or_create(self, sheet_id: UUID, index: tuple[int, int]) -> Cell:
        try:
            return self.get_by_index(sheet_id, index)
        except LookupError:
            cell = Cell(index=index, value=None, sheet_id=sheet_id)
            self.add(cell)
            return cell

    def get_filtred(self, filter_by: dict, order_by: list[str] = None, asc=True) -> list[Cell]:
        result = []
        for cell in self._data:
            if all(cell.__getattribute__(key) == value for key, value in filter_by.items()):
                result.append(cell)
        if len(result) == 0:
            logger.warning(f"get_filtred => len(result) = 0")

        if order_by is not None:
            if order_by[0] == "index":
                result = sorted(result, key=lambda x: (x.index[1], x.index[0]))

        return result

    def get_filtred_as_cell_values_table(self, columns: int, filter_by: dict, order_by: list[str] = None,
                                         asc=True) -> list[list[CellValue]]:
        cells = self.get_filtred(filter_by, order_by, asc)
        table = []
        start = 0
        end = columns
        for i in range(0, columns):
            row = []
            for cell in cells[start:end]:
                row.append(cell.value)
            table.append(row)
            start += columns
            end += columns

        for row in table:
            print(row)
        stop
        return table

    def update(self, data: Cell):
        for i, cell in enumerate(self._data):
            if cell.uuid == data.uuid:
                self._data[i] = data
                return
        raise LookupError
