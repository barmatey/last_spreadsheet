from typing import Union
from uuid import UUID, uuid4

import pandas as pd
from pydantic import Field

from .entity import Formula
from .repository import FormulaRepo
from ..abstract.cell_value import CellTable
from ..abstract.pubsub import Pubsub


class SortedTable(Formula):
    unsorted_data: CellTable = Field(default_factory=list)
    sorted_data: CellTable = Field(default_factory=list)
    asc: bool = True
    subs: list[Pubsub] = Field(default_factory=list)
    uuid: UUID = Field(default_factory=uuid4)


class SortedTablePubsub(Pubsub):
    def __init__(self, entity: SortedTable, repo: FormulaRepo):
        self._repo = repo
        self._entity = entity

    def notify(self):
        raise NotImplemented

    def subscribe(self, sub: Union['Pubsub', list['Pubsub']]):
        raise NotImplemented

    def on_subscribe(self, data: CellTable):
        self._entity.unsorted_data.extend(data)

    def on_update(self, old_data: CellTable, new_data: CellTable):
        raise NotImplemented

    def on_complete(self):
        self.__sort_table()
        self._repo.update(self._entity)

    def __sort_table(self):
        table = pd.DataFrame(self._entity.unsorted_data)
        table = table.sort_values(list(table.columns), ascending=self._entity.asc).values
        self._entity.sorted_data = table
