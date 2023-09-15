from copy import copy
from uuid import UUID, uuid4

from src.spreadsheet.abstract.cell_value import CellValue

from .entity import Cell
from .repository import CellRepo


class UpdateCellValue:
    def __init__(self, sheet_id: UUID, index: tuple[int, int], value: CellValue, repo: CellRepo):
        self._repo = repo
        self._new_value = value
        self._old_cell = self._repo.get_by_index_or_create(sheet_id, index)
        self._new_cell = copy(self._old_cell)

    def execute(self):
        self._new_cell.value = self._new_value
        self._repo.update(self._new_cell)
        return self

    def notify(self):
        for sub in self._new_cell.subs:
            sub.on_update([[self._old_cell.value]], [[self._new_cell.value]])
        for sub in self._new_cell.subs:
            sub.on_complete()


class CreateTable:
    def __init__(self, sheet_id: UUID, size: tuple[int, int], repo: CellRepo):
        self._repo = repo
        self._size = size
        self._sheet_id = sheet_id

    def execute(self):
        table = []
        for i in range(0, self._size[0]):
            row = []
            for j in range(0, self._size[1]):
                cell = Cell(index=(i, j), value=None, sheet_id=self._sheet_id)
                row.append(cell)
                self._repo.add(cell)
            table.append(row)
        return table
