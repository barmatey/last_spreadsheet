from typing import Union
from uuid import UUID, uuid4

from loguru import logger
from pydantic import Field

from spreadsheet.abstract.cell_value import CellTable
from spreadsheet.abstract.pubsub import Pubsub
from spreadsheet.formula.entity import Formula
from spreadsheet.formula.repository import FormulaRepo
from spreadsheet.wire.entity import Ccol, Wire


class PlanItems(Formula):
    subs: list[Pubsub] = Field(default_factory=list)
    uniques: dict[str, int] = Field(default_factory=dict)
    utable: CellTable = Field(default_factory=list)
    ccols: list[Ccol] = Field(default_factory=list)
    uuid: UUID = Field(default_factory=uuid4)

    def __repr__(self):
        return f"PlanItems"

    def partial_copy(self) -> 'PlanItems':
        return self.__class__(
            uuid=self.uuid,
            subs=self.subs,
            utable=self.utable.copy(),
            uniques=self.uniques.copy(),
            ccols=self.ccols.copy(),
        )


class PlanItemsPubsub(Pubsub):
    def __init__(self, entity: PlanItems, repo: FormulaRepo):
        self._old_entity = entity
        self._new_entity = entity.partial_copy()
        self._repo = repo

    def get_entity(self):
        return self._new_entity

    def notify(self):
        for sub in self._new_entity.subs:
            sub.on_before_start()
            sub.on_update(self._old_entity.utable, self._new_entity.utable)
            sub.on_complete()

    def subscribe(self, subs: Union['Pubsub', list['Pubsub']]):
        if not isinstance(subs, list):
            subs = [subs]
        for sub in subs:
            self._new_entity.subs.append(sub)
            sub.on_before_start()
            sub.on_subscribe(self._new_entity.utable)
            sub.on_complete()
        self._repo.update(self._new_entity)

    def on_before_start(self):
        self._old_entity = self._new_entity.partial_copy()

    def on_subscribe(self, data: Wire):
        row = [data.__getattribute__(ccol) for ccol in self._new_entity.ccols]
        key = str(row)
        if self._new_entity.uniques.get(key) is None:
            self._new_entity.utable.append(row)
            self._new_entity.uniques[key] = 1
        else:
            self._new_entity.uniques[key] += 1

    def on_update(self, old_data: Wire, new_data: Wire):
        old_row = [old_data.__getattribute__(ccol) for ccol in self._new_entity.ccols]
        old_key = str(old_row)

        new_row = [new_data.__getattribute__(ccol) for ccol in self._new_entity.ccols]
        new_key = str(new_row)

        # Drop old value
        utable = self._new_entity.utable
        self._new_entity.uniques[old_key] -= 1
        if self._new_entity.uniques[old_key] == 0:
            del self._new_entity.uniques[old_key]
            for i, row in enumerate(utable):
                if str(row) == old_key:
                    del utable[i]

        if self._new_entity.uniques.get(new_key) is not None:
            self._new_entity.uniques[new_key] += 1
            return
        self._new_entity.uniques[new_key] = 1
        utable.append(new_row)

    def on_complete(self):
        self._repo.update(self._new_entity)
        logger.debug(f"PlanItemsPubsub.on_complete() => updating subs: {self._new_entity.subs}")
        self.notify()
