from uuid import UUID, uuid4

from pydantic import Field

from spread.abstract.pubsub import Subscriber, Pubsub
from spread.abstract.pydantic_model import PydanticModel
from spread.wire.model import Ccol, Wire


class PlanItems(PydanticModel):
    subs: list[Subscriber] = Field(default_factory=list)
    uniques: dict[str, Wire] = Field(default_factory=dict)
    ccols: list[Ccol] = Field(default_factory=list)
    uuid: UUID = Field(default_factory=uuid4)


class PlanItemsNode(Pubsub):
    def __init__(self, model: PlanItems):
        self._model = model

    def on_before_start(self):
        pass

    def on_subscribe(self, data: PydanticModel):
        if isinstance(data, Wire):
            pass

    def on_update(self, old_data: PydanticModel, new_data: PydanticModel):
        pass

    def on_complete(self):
        pass

    def notify(self):
        pass

    def subscribe(self, subs: list[Subscriber]):
        pass
