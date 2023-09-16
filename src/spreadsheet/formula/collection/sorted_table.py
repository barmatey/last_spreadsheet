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

    def partial_copy(self):
        return self.__class__(
            uuid=self.uuid,
            unsorted_data=self.unsorted_data.copy(),
            sorted_data=self.sorted_data.copy(),
            asc=self.asc,
            subs=self.subs,
        )


class SortedTablePubsub(Pubsub):
    def __init__(self, entity: SortedTable, repo: FormulaRepo):
        self._repo = repo
        self._old_entity = entity
        self._new_entity = entity.model_copy()

    def __repr__(self):
        return "SortedTablePubsub"

    def get_entity(self):
        return self._new_entity

    def notify(self):
        for sub in self._new_entity.subs:
            sub.on_update(self._old_entity.sorted_data, self._new_entity.sorted_data)
        for sub in self._new_entity.subs:
            sub.on_complete()

    # todo Should I log data in this code?
    def subscribe(self, subs: Union['Pubsub', list['Pubsub']]):
        if not isinstance(subs, list):
            subs = [subs]
        for sub in subs:
            sub.on_subscribe(self._new_entity.sorted_data)
            self._new_entity.subs.append(sub)
        for sub in subs:
            sub.on_complete()

    def on_subscribe(self, data: CellTable):
        self._new_entity.unsorted_data = data

    def on_update(self, old_data: CellTable, new_data: CellTable):
        self._old_entity = self._new_entity.partial_copy()
        self._new_entity.unsorted_data = new_data

    def on_complete(self):
        self.__sort_table()
        self._repo.update(self._new_entity)
        logger.info(f"SortedTablePubsub.on_complete() => updating subs: {self._new_entity.subs}")
        self.notify()

    def __sort_table(self):
        table = pd.DataFrame(self._new_entity.unsorted_data)
        table = table.sort_values(list(table.columns), ascending=self._new_entity.asc).values
        self._new_entity.sorted_data = table
