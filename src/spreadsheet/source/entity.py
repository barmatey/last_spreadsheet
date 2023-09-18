from uuid import UUID, uuid4

from pydantic import Field

from spreadsheet.abstract.pubsub import Pubsub, Subscriber
from spreadsheet.abstract.pydantic_model import PydanticModel
from spreadsheet.broker.event import Event
from spreadsheet.wire.entity import Wire


class Source(PydanticModel):
    uuid: UUID = Field(default_factory=uuid4)
    wires: list[Wire] = Field(default_factory=list)


class SourceNode(PydanticModel, Pubsub):
    value: Source
    subs: list[Subscriber] = Field(default_factory=list)
    events: list[Event] = Field(default_factory=list)
    uuid: UUID = Field(default_factory=uuid4)

    def get_subs(self) -> list[Subscriber]:
        return self.subs

    def parse_events(self) -> list[Event]:
        return self.events
