from typing import Union

from loguru import logger

from spreadsheet.abstract.cell_value import CellTable
from spreadsheet.abstract.pubsub import Pubsub

from .entity import Cell
from .repository import CellRepo
from .usecase import UpdateCellValue
from ..sheet.repository import SheetRepo


class CellPubsub(Pubsub):
    def __init__(self, entity: Cell, cell_repo: CellRepo, sheet_repo: SheetRepo):
        self._usecases: list[UpdateCellValue] = []
        self._entity = entity
        self._cell_repo = cell_repo
        self._sheet_repo = sheet_repo

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
        logger.success(f'old_data: {old_data}')
        logger.success(f'new_data: {new_data}')
        sheet_id = self._entity.sheet_id
        start_row = self._entity.index[0]
        start_col = self._entity.index[1]

        hashed = {}
        for i, row in enumerate(old_data):
            for j in range(0, len(row)):
                index = (start_row + i, start_col + j)
                hashed[index] = UpdateCellValue(sheet_id, index, None, self._cell_repo, self._sheet_repo)
        for i, row in enumerate(new_data):
            for j in range(0, len(row)):
                index = (i, j)
                hashed[index] = UpdateCellValue(sheet_id, index, new_data[i][j], self._cell_repo, self._sheet_repo)

        self._usecases = [u.execute() for u in hashed.values()]

    def on_subscribe(self, data: CellTable):
        if len(data) == 1 and len(data[0]) == 1:
            raise NotImplemented

        sheet_id = self._entity.sheet_id
        start_row = self._entity.index[0]
        start_col = self._entity.index[1]

        for i, row in enumerate(data):
            for j, cell_value in enumerate(row):
                index = (start_row + i, start_col + j)
                self._usecases.append(UpdateCellValue(sheet_id, index, data[i][j], self._cell_repo, self._sheet_repo).execute())

    def on_complete(self):
        logger.info("CellPubsub.on_complete() => updating subs: [...]")
        self.notify()
