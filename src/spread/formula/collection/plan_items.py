from uuid import UUID, uuid4

from loguru import logger
from pydantic import Field

from spread.abstract.cell_value import CellTable
from spread.abstract.pubsub import Subscriber
from spread.abstract.pydantic_model import PydanticModel
from spread.formula.model import Formula
from spread.formula.node import FormulaNode
from spread.wire.entity import Ccol, Wire
from spread.formula.repository import FormulaNodeRepo


class PlanItems(Formula):
    ccols: list[Ccol]
    uniques: dict[str, int] = Field(default_factory=dict)
    utable: CellTable = Field(default_factory=list)
    uuid: UUID = Field(default_factory=uuid4)

    def __repr__(self):
        return f"PlanItems"

    def partial_copy(self):
        return self.__class__(
            subs=self.subs,
            uniques=self.uniques.copy(),
            utable=self.utable.copy(),
            ccols=self.ccols.copy(),
            uuid=self.uuid,
        )


class PlanItemsNode(FormulaNode):
    def __init__(self, value: PlanItems, subs: list[Subscriber] = None, uuid: UUID = None):
        self._value = value
        self._old_value = None
        self._subs = subs if subs is not None else []
        self.uuid = uuid if uuid is not None else uuid4()

    def __repr__(self):
        return "PlanItemsNode"

    def get_value(self) -> PlanItems:
        return self._value

    def on_before_start(self):
        self._old_value = self._value.model_copy(deep=True)

    def on_subscribe(self, data: PydanticModel):
        if not isinstance(data, Wire):
            raise TypeError
        row = [data.__getattribute__(ccol) for ccol in self._value.ccols]
        key = str(row)
        if self._value.uniques.get(key) is None:
            self._value.utable.append(row)
            self._value.uniques[key] = 1
        else:
            self._value.uniques[key] += 1

    def on_update(self, old_data: PydanticModel, new_data: PydanticModel):
        if not isinstance(old_data, Wire):
            raise TypeError
        if not isinstance(new_data, Wire):
            raise TypeError

        old_row = [old_data.__getattribute__(ccol) for ccol in self._value.ccols]
        old_key = str(old_row)

        new_row = [new_data.__getattribute__(ccol) for ccol in self._value.ccols]
        new_key = str(new_row)

        # Drop old value
        utable = self._value.utable
        self._value.uniques[old_key] -= 1
        if self._value.uniques[old_key] == 0:
            del self._value.uniques[old_key]
            for i, row in enumerate(utable):
                if str(row) == old_key:
                    del utable[i]

        if self._value.uniques.get(new_key) is not None:
            self._value.uniques[new_key] += 1
            return
        self._value.uniques[new_key] = 1
        utable.append(new_row)

    def on_complete(self):
        logger.debug(f"PlanItemsPubsub.on_complete() => notify {len(self._subs)} subs")
        self.notify()

    def notify(self):
        for sub in self._subs:
            sub.on_before_start()
            sub.on_update(self._old_value, self._value)
            sub.on_complete()

    def subscribe(self, subs: list[Subscriber]):
        logger.debug(f"PlanItemsNode.subscribe({subs})")
        for sub in subs:
            sub.on_before_start()
            sub.on_subscribe(self._value)
            sub.on_complete()
            self._subs.append(sub)


def create_node(ccols: list[Ccol]) -> PlanItemsNode:
    entity = PlanItems(ccols=ccols)
    node = PlanItemsNode(entity)
    FormulaNodeRepo().add(node)
    return node


def get_node_by_id(uuid: UUID) -> PlanItemsNode:
    node = FormulaNodeRepo().get_by_id(uuid)
    if not isinstance(node, PlanItemsNode):
        raise TypeError
    return node


def save_node(data: PlanItemsNode):
    FormulaNodeRepo().update(data)
