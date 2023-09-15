from uuid import UUID

from .entity import Sheet
from .repository import SheetRepo
from ..abstract.cell_value import CellValue
from ..cell.entity import Cell
from ..cell.repository import CellRepo


class CreateSheet:
    def __init__(self, sheet_id: UUID, title: str, size: tuple[int, int], sheet_repo: SheetRepo, cell_repo: CellRepo):
        self._title = title
        self._sheet_id = sheet_id
        self._size = size
        self._sheet_repo = sheet_repo
        self._cell_repo = cell_repo

    def execute(self):
        sheet = Sheet(uuid=self._sheet_id, size=self._size, title=self._title)
        self._sheet_repo.add(sheet)
        for i in range(0, self._size[0]):
            for j in range(0, self._size[1]):
                cell = Cell(index=(i, j), value=None, sheet_id=self._sheet_id)
                self._cell_repo.add(cell)


class UpdateCellValue:
    def __init__(self, sheet_id: UUID, index: tuple[int, int], value: CellValue,
                 sheet_repo: SheetRepo, cell_repo: CellRepo):
        self._sheet_id = sheet_id
        self._index = index
        self._value = value
        self._sheet_repo = sheet_repo
        self._cell_repo = cell_repo

    def execute(self):
        raise NotImplemented
