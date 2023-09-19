from uuid import UUID, uuid4

from loguru import logger
from pydantic import Field

from broker.messagebus import MessageBus
from spread.abstract.pubsub import Subscriber
from spread.abstract.pydantic_model import PydanticModel
from spread.formula.collection.plan_items.entity import PlanItems
from spread.formula.collection.report_filter.events import ReportFilterDestroyed
from spread.formula.model import Formula
from spread.formula.node import FormulaNode


class ReportFilter(Formula):
    index: int
    filter_by: dict = Field(default_factory=dict)
    uuid: UUID = Field(default_factory=uuid4)


class ReportFilterNode(FormulaNode):
    def __init__(self, value: ReportFilter, parents_count=0, subs: list[Subscriber] = None, uuid: UUID = None):
        super().__init__(uuid)
        self._value = value
        self._old_value = None
        self._subs = subs if subs is not None else []
        self._parents_count = parents_count
        self.uuid = uuid if uuid is not None else uuid4()
        self._messagebus = MessageBus()

    def __repr__(self):
        return "ReportFilterNode"

    def get_value(self) -> ReportFilter:
        return self._value

    def on_before_start(self):
        self._old_value = self._value.model_copy(deep=True)

    def on_subscribe(self, data: PydanticModel):
        if not isinstance(data, PlanItems):
            raise TypeError
        index = self._value.index
        filter_by = {}
        for j, ccol in enumerate(data.ccols):
            filter_by[ccol] = data.utable[index][j]
        self._value.filter_by = filter_by
        self._parents_count += 1

    def on_unsubscribe(self):
        self._parents_count -= 1
        if self._parents_count == 0:
            self._messagebus.push_event(ReportFilterDestroyed(self))

    def on_update(self, old_data: PydanticModel, new_data: PydanticModel):
        if not isinstance(old_data, PlanItems):
            raise TypeError(type(old_data))
        if not isinstance(new_data, PlanItems):
            raise TypeError(type(new_data))
        self.on_subscribe(new_data)

    def on_complete(self):
        logger.debug(f"ReportFilterNode.on_complete() => notify {len(self._subs)} subs")
        self.notify()

    def notify(self):
        pass

    def subscribe(self, subs: list[Subscriber]):
        raise NotImplemented

    def unsubscribe(self, subs: list[Subscriber]):
        raise NotImplemented
