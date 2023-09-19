from uuid import UUID, uuid4

from loguru import logger
from pydantic import Field

from spreadsheet.abstract.pubsub import Pubsub, Subscriber
from spreadsheet.abstract.pydantic_model import PydanticModel
from spreadsheet.abstract.event import Event
from spreadsheet.wire.entity import Wire


class Source(PydanticModel):
    uuid: UUID = Field(default_factory=uuid4)
    wires: list[Wire] = Field(default_factory=list)


class SourceNode(PydanticModel, Pubsub):
    value: Source
    subs: list[Subscriber] = Field(default_factory=list)
    events: list[Event] = Field(default_factory=list)
    uuid: UUID = Field(default_factory=uuid4)

    def on_before_start(self):
        pass

    def on_subscribe(self, data: PydanticModel):
        if not isinstance(data, Wire):
            raise TypeError
        self.value.wires.append(data)

    def on_complete(self):
        logger.debug("SourceNode.on_complete()")

    def subscribe(self, subs: list[Subscriber]):
        raise NotImplemented

    def get_subs(self) -> list[Subscriber]:
        return self.subs

    def parse_events(self) -> list[Event]:
        events = self.events
        self.events = []
        return events
