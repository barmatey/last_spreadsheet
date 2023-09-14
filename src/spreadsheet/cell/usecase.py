from uuid import UUID, uuid4

from .entity import Cell
from .repository import CellRepo
from ..abstract.cell_value import CellTable


class CreateTable:
    def __init__(self, repo: CellRepo):
        self._repo = repo
        self._size = (0, 0)
        self._values = None
        self._sheet_id = uuid4()

    def set_size(self, size: tuple[int, int]):
        self._size = size
        return self

    def set_values(self, values: CellTable):
        self._values = values
        return self

    def set_sheet_id(self, uuid: UUID):
        self._sheet_id = uuid
        return self

    def create(self):
        table = []
        for i in range(0, self._size[0]):
            row = []
            for j in range(0, self._size[1]):
                cell = Cell(index=(i, j), value=self._values[i][j], sheet_id=self._sheet_id)
                row.append(cell)
                self._repo.add(cell)
            table.append(row)
        return table
