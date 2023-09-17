from typing import Union
from uuid import UUID, uuid4

from loguru import logger
from pydantic import Field

from spreadsheet.abstract.cell_value import CellValue
from spreadsheet.abstract.pubsub import Pubsub
from spreadsheet.formula.bootstrap import FormulaBootstrap
from spreadsheet.formula.entity import Formula
from spreadsheet.formula.repository import FormulaRepo
from spreadsheet.wire.entity import Wire


class SumFiltred(Formula):
    sum: float = 0
    subs: list[Pubsub] = Field(default_factory=list)
    filters: dict[str, CellValue] = Field(default_factory=dict)
    uuid: UUID = Field(default_factory=uuid4)


class SumFiltredPubsub(Pubsub):
    def __init__(self, entity: SumFiltred):
        self._new_entity = entity
        self._old_value = None

        self._repo: FormulaRepo = FormulaBootstrap().get_repo()

    def get_entity(self):
        return self._new_entity

    def notify(self):
        for sub in self._new_entity.subs:
            sub.on_before_start()
            sub.on_update([[self._old_value]], [[self._new_entity.sum]])
            sub.on_complete()

    def subscribe(self, subs: Union['Pubsub', list['Pubsub']]):
        if not isinstance(subs, list):
            subs = [subs]
        for sub in subs:
            self._new_entity.subs.append(sub)
            sub.on_before_start()
            sub.on_subscribe([[self._new_entity.sum]])
            sub.on_complete()
        self._repo.update(self._new_entity)

    def on_before_start(self):
        self._old_value = self._new_entity.sum

    def on_subscribe(self, data: Wire):
        if all(data.__getattribute__(key) == value for key, value in self._new_entity.filters.items()):
            self._new_entity.sum += data.amount

    def on_update(self, old_data: Wire, new_data: Wire):
        if all(old_data.__getattribute__(key) == value for key, value in self._new_entity.filters.items()):
            self._new_entity.sum -= old_data.amount
        if all(new_data.__getattribute__(key) == value for key, value in self._new_entity.filters.items()):
            self._new_entity.sum += new_data.amount

    def on_complete(self):
        self._repo.update(self._new_entity)
        self.notify()
