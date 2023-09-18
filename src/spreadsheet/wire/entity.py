from uuid import UUID, uuid4

from pydantic import Field

from spread.abstract.pydantic_model import PydanticModel
from spread.messagebus import Event
from spreadsheet.abstract.pubsub import Pubsub, Subscriber


class Wire(PydanticModel):
    uuid: UUID = Field(default_factory=uuid4)


class WireNode(Pubsub, PydanticModel):
    value: Wire
    subs: list[Subscriber]
    events: list[Event] = Field(default_factory=list)
    uuid: UUID = Field(default_factory=uuid4)

    def get_subs(self) -> list[Subscriber]:
        return self.subs

    def parse_events(self) -> list[Event]:
        events = self.events
        self.events = []
        return events
