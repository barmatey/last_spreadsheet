from uuid import UUID, uuid4

from loguru import logger
from pydantic import Field

from spread.abstract.pubsub import Pubsub, Subscriber
from spread.abstract.pydantic_model import PydanticModel
from spread.formula.collection.plan_items import PlanItems
from spread.formula.model import Formula
from spread.formula.repository import FormulaNodeRepo
from spread.wire.entity import Ccol


class ReportFilter(Formula):
    index: int
    filter_by: dict = Field(default_factory=dict)
    subs: list[Subscriber] = Field(default_factory=list)
    uuid: UUID = Field(default_factory=uuid4)


class ReportFilterNode(Pubsub):
    def __init__(self, model: ReportFilter):
        self._model = model
        self._formula_repo: FormulaNodeRepo = FormulaNodeRepo()

    def __repr__(self):
        return "ReportFilterNode"

    def on_before_start(self):
        pass

    def on_subscribe(self, data: PydanticModel):
        if not isinstance(data, PlanItems):
            raise TypeError
        index = self._model.index
        filter_by = {}
        for j, ccol in enumerate(data.ccols):
            filter_by[ccol] = data.utable[index][j]
        self._model.filter_by = filter_by

    def on_update(self, old_data: PydanticModel, new_data: PydanticModel):
        logger.warning("ReportFilterNode.on_update() not implemented")
        # del self._model

    def on_complete(self):
        logger.debug(f"ReportFilterNode.on_complete() => notify {len(self._model.subs)} subs")
        self._formula_repo.update(self._model)
        self.notify()

    def notify(self):
        pass

    def subscribe(self, subs: list[Subscriber]):
        raise NotImplemented
