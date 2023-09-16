from uuid import UUID, uuid4

from loguru import logger

from src.spreadsheet.abstract.cell_value import CellValue
from .bootstrap import CellBootstrap

from .entity import Cell
from .repository import CellRepo
from ..abstract.pubsub import Subscriber
from ..sheet.bootstrap import SheetBootstrap
from ..sheet.repository import SheetRepo


class AppendSubscribers:
    def __init__(self, cell: Cell, subs: Subscriber | list[Subscriber]):
        self._cell = cell
        self._subs = [subs] if not isinstance(subs, list) else subs

    def execute(self):
        for sub in self._subs:
            self._cell.subs.append(sub)
            sub.on_before_start()
            sub.on_subscribe([[self._cell.value]])
            sub.on_complete()
        return self

    def save(self):
        cell_repo: CellRepo = CellBootstrap().get_repo()
        cell_repo.update(self._cell)


class UpdateCellValue:
    def __init__(self, sheet_id: UUID, index: tuple[int, int], value: CellValue):
        self._cell_repo: CellRepo = CellBootstrap().get_repo()
        self._sheet_repo: SheetRepo = SheetBootstrap().get_repo()

        self._old_cell = self._get_cell_or_expand_sheet(sheet_id, index)
        self._new_cell = self._old_cell.partial_copy()
        self._new_value = value

    def _get_cell_or_expand_sheet(self, sheet_id: UUID, index: tuple[int, int]) -> Cell:
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
                sheet.size = (index[0], sheet.size[1])
                self._sheet_repo.update(sheet)
                return self._cell_repo.get_by_index(sheet_id, index)
            if sheet.size[1] <= index[1]:
                for i in range(0, sheet.size[0] + 1):
                    for j in range(sheet.size[1], index[1] + 1):
                        cell = Cell(index=(i, j), value=None, sheet_id=sheet_id)
                        self._cell_repo.add(cell)
                sheet.size = (sheet.size[0], index[1])
                self._sheet_repo.update(sheet)
                return self._cell_repo.get_by_index(sheet_id, index)
            raise Exception

    def execute(self):
        self._new_cell.value = self._new_value
        return self

    def save(self):
        self._cell_repo.update(self._new_cell)
        return self

    def notify(self):
        for sub in self._new_cell.subs:
            sub.on_before_start()
            sub.on_update([[self._old_cell.value]], [[self._new_cell.value]])
            sub.on_complete()
