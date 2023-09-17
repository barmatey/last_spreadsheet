from typing import Union
from uuid import UUID, uuid4

from pydantic import Field

from spreadsheet.abstract.cell_value import CellValue, CellTable
from spreadsheet.abstract.pubsub import Pubsub
from spreadsheet.formula.bootstrap import FormulaBootstrap
from spreadsheet.formula.entity import Formula
from spreadsheet.formula.repository import FormulaRepo
from spreadsheet.wire.entity import Wire, Ccol


class ReportFilter(Formula):
    subs: list[Pubsub] = Field(default_factory=list)
    filters: dict[str, CellValue] = Field(default_factory=dict)
    ccols: list[Ccol] = Field(default_factory=list)
    uuid: UUID = Field(default_factory=uuid4)

    def partial_copy(self):
        return self.__class__(
            uuid=self.uuid,
            subs=self.subs.copy(),
            ccols=self.ccols.copy(),
            filters=self.filters.copy(),
        )


class ReportFilterPubsub(Pubsub):
    def __init__(self, entity: ReportFilter):
        self._repo: FormulaRepo = FormulaBootstrap().get_repoo()

        self._new_entity = entity.partial_copy()
        self._old_entity = entity

    def get_entity(self):
        pass

    def notify(self):
        # for sub in self._new_entity.subs:
        #     sub.on_before_start()
        #     sub.on_update()
        #     sub.on_complete()
        pass

    def subscribe(self, subs: Union['Pubsub', list['Pubsub']]):
        if not isinstance(subs, list):
            subs = [subs]
        for sub in subs:
            raise NotImplemented
        self._repo.update(self._new_entity)

    def on_before_start(self):
        self._old_entity = self._new_entity.partial_copy()

    def on_subscribe(self, data: CellTable):
        filters = {}
        for row in data:
            for j, cell in enumerate(row):
                filters[self._new_entity.ccols[j]] = cell
        self._new_entity.filters = filters

    def on_update(self, old_data: CellTable, new_data: CellTable):
        self.on_subscribe(new_data)

    def on_complete(self):
        self._repo.update(self._new_entity)
        self.notify()
