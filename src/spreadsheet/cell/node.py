from typing import Union

from loguru import logger

from spreadsheet.abstract.cell_value import CellTable
from spreadsheet.abstract.pubsub import Pubsub

from .entity import Cell
from .repository import CellRepo
from .usecase import UpdateCellValue


class CellPubsub(Pubsub):
    def __init__(self, entity: Cell, repo: CellRepo):
        self._usecases: list[UpdateCellValue] = []
        self._entity = entity
        self._repo = repo

    def __repr__(self):
        return f"CellPubsub"

    def get_entity(self) -> Cell:
        return self._entity

    def notify(self):
        for usecase in self._usecases:
            usecase.notify()

    def subscribe(self, sub: Union['Pubsub', list['Pubsub']]):
        raise NotImplemented

    def on_update(self, old_data: CellTable, new_data: CellTable):
        self.on_subscribe(new_data)

    def on_subscribe(self, data: CellTable):
        if len(data) == 1 and len(data[0]) == 1:
            raise NotImplemented

        sheet_id = self._entity.sheet_id
        start_row = self._entity.index[0]
        start_col = self._entity.index[1]
        for i, row in enumerate(data):
            for j, cell_value in enumerate(row):
                index = (start_row + i, start_col + j)
                self._usecases.append(UpdateCellValue(sheet_id, index, data[i][j], self._repo).execute())

    def on_complete(self):
        logger.info("CellPubsub.on_complete() => updating subs: [...]")
        self.notify()
