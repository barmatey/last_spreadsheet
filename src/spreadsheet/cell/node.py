from typing import Union

from loguru import logger

from spreadsheet.abstract.cell_value import CellTable
from spreadsheet.abstract.pubsub import Pubsub

from .entity import Cell
from .usecase import UpdateCellValue, AppendSubscribers


class CellPubsub(Pubsub):
    def __init__(self, entity: Cell):
        self._new_entity = entity.partial_copy()
        self._usecases: list[UpdateCellValue] = []

    def __repr__(self):
        return "CellPubsub"

    def get_entity(self):
        return self._new_entity

    def notify(self):
        for u in self._usecases:
            u.notify()

    def subscribe(self, subs: Union['Pubsub', list['Pubsub']]):
        AppendSubscribers(self._new_entity, subs).execute().save()

    def on_before_start(self):
        pass

    def on_update(self, old_data: CellTable, new_data: CellTable):
        sheet_id = self._new_entity.sheet_id
        start_row = self._new_entity.index[0]
        start_col = self._new_entity.index[1]

        hashed = {}
        for i, row in enumerate(old_data):
            for j in range(0, len(row)):
                index = (start_row + i, start_col + j)
                hashed[index] = UpdateCellValue(sheet_id, index, None)
        for i, row in enumerate(new_data):
            for j in range(0, len(row)):
                index = (start_row + i, start_col + j)
                hashed[index] = UpdateCellValue(sheet_id, index, new_data[i][j])
        self._usecases = hashed.values()

    def on_subscribe(self, data: CellTable):
        sheet_id = self._new_entity.sheet_id
        start_row = self._new_entity.index[0]
        start_col = self._new_entity.index[1]

        for i, row in enumerate(data):
            for j, cell_value in enumerate(row):
                index = (start_row + i, start_col + j)
                self._usecases.append(
                    UpdateCellValue(sheet_id, index, data[i][j])
                )

    def on_complete(self):
        for u in self._usecases:
            logger.info(f"CellPubsub("
                        f"sheet_id={u._new_cell.sheet_id}, "
                        f"index={u._new_cell.index}, "
                        f"value={u._new_cell.value}"
                        f").on_complete() "
                        f"=> updating subs: [...]")
            u.execute().save()
        self.notify()
