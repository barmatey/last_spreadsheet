from copy import copy
from uuid import UUID, uuid4

from src.spreadsheet.abstract.cell_value import CellValue

from .entity import Cell
from .repository import CellRepo
from ..sheet.repository import SheetRepo


class UpdateCellValue:
    def __init__(self, sheet_id: UUID, index: tuple[int, int], value: CellValue,
                 cell_repo: CellRepo, sheet_repo: SheetRepo):
        self._cell_repo = cell_repo
        self._sheet_repo = sheet_repo
        self._new_value = value
        self._old_cell = self._get_cell_or_expand_sheet(sheet_id, index)
        self._new_cell = copy(self._old_cell)

    def _get_cell_or_expand_sheet(self, sheet_id: UUID, index: tuple[int, int]):
        try:
            cell = self._cell_repo.get_by_index(sheet_id, index)
            return cell
        except LookupError:
            sheet = self._sheet_repo.get_by_id(sheet_id)
            if sheet.size[0] <= index[0]:
                for i in range(sheet.size[0], index[0] + 1):
                    for j in range(0, sheet.size[1] + 1):
                        cell = Cell(index=(i, j), value=None, sheet_id=sheet_id)
                        self._cell_repo.add(cell)
                return self._cell_repo.get_by_index(sheet_id, index)
            if sheet.size[1] <= index[1]:
                for i in range(0, sheet.size[0] + 1):
                    for j in range(sheet.size[1], index[1] + 1):
                        cell = Cell(index=(i, j), value=None, sheet_id=sheet_id)
                        self._cell_repo.add(cell)
                return self._cell_repo.get_by_index(sheet_id, index)
            raise Exception

    def execute(self):
        self._new_cell.value = self._new_value
        self._cell_repo.update(self._new_cell)
        return self

    def notify(self):
        for sub in self._new_cell.subs:
            sub.on_update([[self._old_cell.value]], [[self._new_cell.value]])
        for sub in self._new_cell.subs:
            sub.on_complete()


class CreateTable:
    def __init__(self, sheet_id: UUID, size: tuple[int, int], cell_repo: CellRepo):
        self._cell_repo = cell_repo
        self._size = size
        self._sheet_id = sheet_id

    def execute(self):
        table = []
        for i in range(0, self._size[0]):
            row = []
            for j in range(0, self._size[1]):
                cell = Cell(index=(i, j), value=None, sheet_id=self._sheet_id)
                row.append(cell)
                self._cell_repo.add(cell)
            table.append(row)
        return table
