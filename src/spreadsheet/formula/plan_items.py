from typing import Union
from uuid import UUID, uuid4

from pydantic import Field

from spreadsheet.abstract.cell_value import CellTable
from spreadsheet.abstract.pubsub import Pubsub
from spreadsheet.formula.entity import Formula
from spreadsheet.formula.repository import FormulaRepo


class PlanItems(Formula):
    subs: list[Pubsub] = Field(default_factory=list)
    uniques: dict[str, int] = Field(default_factory=dict)
    utable: CellTable = Field(default_factory=list)
    uuid: UUID = Field(default_factory=uuid4)

    def __repr__(self):
        return f"PlanItems"


class PlanItemsPubsubUsecase(Pubsub):
    def __init__(self, entity: PlanItems, repo: FormulaRepo):
        self._entity = entity
        self._repo = repo

    def subscribe(self, subs: Union['Pubsub', list['Pubsub']]):
        if not isinstance(subs, list):
            subs = [subs]
        for sub in subs:
            sub.on_next(self._entity.utable)
        for sub in subs:
            sub.on_complete()

    def on_next(self, data: CellTable):
        row = data[0]
        key = str(row)
        if self._entity.uniques.get(key) is None:
            self._entity.utable.append(row)
            self._entity.uniques[key] = 1
        else:
            self._entity.uniques[key] += 1

    def on_complete(self):
        self._repo.update(self._entity)
