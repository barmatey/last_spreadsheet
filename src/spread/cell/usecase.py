from uuid import UUID

from spread.cell.model import CellValue


class UpdateCellValue:
    def __init__(self, sheet_id: UUID, index: tuple[int, int], value: CellValue):

        self._old_cell = self._get_cell_or_expand_sheet(sheet_id, index)
        self._new_cell = self._old_cell.partial_copy()
        self._new_value = value


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
