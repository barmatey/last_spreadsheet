from copy import copy, deepcopy
from typing import Union
from uuid import UUID, uuid4

import pandas as pd
from loguru import logger
from pydantic import Field

from spreadsheet.formula.entity import Formula
from spreadsheet.formula.repository import FormulaRepo
from spreadsheet.abstract.cell_value import CellTable
from spreadsheet.abstract.pubsub import Pubsub


class SortedTable(Formula):
    unsorted_data: CellTable = Field(default_factory=list)
    sorted_data: CellTable = Field(default_factory=list)
    asc: bool = True
    subs: list[Pubsub] = Field(default_factory=list)
    uuid: UUID = Field(default_factory=uuid4)


class SortedTablePubsub(Pubsub):
    def __init__(self, entity: SortedTable, repo: FormulaRepo):
        self._repo = repo
        self._old_entity = entity
        self._new_entity = SortedTable(
            uuid=entity.uuid,
            unsorted_data=deepcopy(entity.unsorted_data),
            sorted_data=deepcopy(entity.sorted_data),
            asc=entity.asc,
            subs=entity.subs,
        )

    def __repr__(self):
        return "SortedTablePubsub"

    def get_entity(self):
        return self._new_entity

    def notify(self):
        raise NotImplemented

    def subscribe(self, sub: Union['Pubsub', list['Pubsub']]):
        raise NotImplemented

    def on_subscribe(self, data: CellTable):
        self._new_entity.unsorted_data = data

    def on_update(self, old_data: CellTable, new_data: CellTable):
        self._new_entity.unsorted_data = new_data

    def on_complete(self):
        self.__sort_table()
        self._repo.update(self._new_entity)
        logger.info(f"SortedTablePubsub.on_complete() => updating subs: {self._new_entity.subs}")

    def __sort_table(self):
        table = pd.DataFrame(self._new_entity.unsorted_data)
        table = table.sort_values(list(table.columns), ascending=self._new_entity.asc).values
        self._new_entity.sorted_data = table
