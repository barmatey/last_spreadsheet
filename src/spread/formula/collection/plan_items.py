from uuid import UUID, uuid4

from loguru import logger
from pydantic import Field

from spread.abstract.cell_value import CellTable
from spread.abstract.pubsub import Subscriber, Pubsub
from spread.abstract.pydantic_model import PydanticModel
from spread.formula.model import Formula
from spread.formula.repository import FormulaRepo
from spread.wire.model import Ccol, Wire


class PlanItems(Formula):
    ccols: list[Ccol]
    subs: list[Subscriber] = Field(default_factory=list)
    uniques: dict[str, int] = Field(default_factory=dict)
    utable: CellTable = Field(default_factory=list)
    uuid: UUID = Field(default_factory=uuid4)

    def __repr__(self):
        return f"PlanItems"

    def partial_copy(self):
        return self.__class__(
            subs=self.subs.copy(),
            uniques=self.uniques.copy(),
            ccols=self.ccols.copy(),
            uuid=self.uuid,
        )


class PlanItemsNode(Pubsub):
    def __init__(self, model: PlanItems):
        self._model = model.partial_copy()
        self._old_model = model

        self._formula_repo: FormulaRepo = FormulaRepo()

    def __repr__(self):
        return "PlanItemsNode"

    def on_before_start(self):
        self._old_model = self._model.partial_copy()

    def on_subscribe(self, data: PydanticModel):
        if not isinstance(data, Wire):
            raise TypeError
        row = [data.__getattribute__(ccol) for ccol in self._model.ccols]
        key = str(row)
        if self._model.uniques.get(key) is None:
            self._model.utable.append(row)
            self._model.uniques[key] = 1
        else:
            self._model.uniques[key] += 1

    def on_update(self, old_data: PydanticModel, new_data: PydanticModel):
        if not isinstance(old_data, Wire):
            raise TypeError
        if not isinstance(new_data, Wire):
            raise TypeError

        old_row = [old_data.__getattribute__(ccol) for ccol in self._model.ccols]
        old_key = str(old_row)

        new_row = [new_data.__getattribute__(ccol) for ccol in self._model.ccols]
        new_key = str(new_row)

        # Drop old value
        utable = self._model.utable
        self._model.uniques[old_key] -= 1
        if self._model.uniques[old_key] == 0:
            del self._model.uniques[old_key]
            for i, row in enumerate(utable):
                if str(row) == old_key:
                    del utable[i]

        if self._model.uniques.get(new_key) is not None:
            self._model.uniques[new_key] += 1
            return
        self._model.uniques[new_key] = 1
        utable.append(new_row)

    def on_complete(self):
        logger.debug(f"PlanItemsPubsub.on_complete() => update {len(self._model.subs)} subs")
        self._formula_repo.update(self._model)
        self.notify()

    def notify(self):
        for sub in self._model.subs:
            sub.on_before_start()
            sub.on_update(self._old_model, self._model)
            sub.on_complete()

    def subscribe(self, subs: list[Subscriber]):
        for sub in subs:
            sub.on_before_start()
            sub.on_update(self._old_model, self._model)
            sub.on_complete()
            self._model.subs.append(sub)
        self._formula_repo.update(self._model)
