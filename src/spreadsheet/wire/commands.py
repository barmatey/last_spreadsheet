from datetime import datetime
from uuid import uuid4, UUID

from loguru import logger
from pydantic import Field

from spreadsheet.broker.command import Command
from spreadsheet.broker.event import Event

from spreadsheet.source import usecases as source_usecase
from spreadsheet.wire import usecases as wire_usecase


class CreateWireNode(Command):
    source_id: UUID
    sender: float
    receiver: float
    amount: float
    sub1: str = ""
    sub2: str = ""
    comment: str = ""
    currency: str = "RUB"
    date: datetime = Field(default_factory=datetime.now)
    uuid: UUID = Field(default_factory=uuid4)
    result: UUID | None = None
    new_events: list[Event] = Field(default_factory=list)

    def execute(self):
        logger.info("CreateWireNode.execute()")
        # Create
        source_node = source_usecase.get_node_by_id(self.source_id)
        wire_node = wire_usecase.create_node(self.model_dump(exclude={"_result", "source_id"}))
        wire_node.subscribe([source_node])

        # Save
        source_usecase.save_node(source_node)
        wire_usecase.save_node(wire_node)

        self.new_events.extend(source_node.parse_events())
        self.result = wire_node.uuid

    def get_uuid(self) -> UUID:
        return self.uuid

    def get_result(self):
        return self.result

    def parse_new_events(self) -> list[Event]:
        events = self._new_events
        self.new_events = []
        return events
