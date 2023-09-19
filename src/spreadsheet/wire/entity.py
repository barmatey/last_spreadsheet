from uuid import UUID, uuid4

from loguru import logger
from pydantic import Field

from spreadsheet.abstract.pydantic_model import PydanticModel
from spreadsheet.abstract.pubsub import Pubsub, Subscriber
from spreadsheet.abstract.event import Event


class Wire(PydanticModel):
    uuid: UUID = Field(default_factory=uuid4)


class WireNode(Pubsub, PydanticModel):
    value: Wire
    subs: list[Subscriber]
    events: list[Event] = Field(default_factory=list)
    uuid: UUID = Field(default_factory=uuid4)

    def on_before_start(self):
        pass

    def on_subscribe(self, data: PydanticModel):
        logger.debug("WireNode.on_subscribe()")

    def on_complete(self):
        pass

    def subscribe(self, subs: list[Subscriber]):
        for sub in subs:
            sub.on_before_start()
            sub.on_subscribe(self.value)
            sub.on_complete()
            self.subs.append(sub)

    def get_subs(self) -> list[Subscriber]:
        return self.subs

    def parse_events(self) -> list[Event]:
        events = self.events
        self.events = []
        return events
