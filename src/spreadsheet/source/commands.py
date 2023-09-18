from uuid import UUID, uuid4

from loguru import logger
from pydantic import Field

from spreadsheet.broker.command import Command
from spreadsheet.broker.event import Event
from . import usecases


class CreateSourceNode(Command):
    uuid: UUID = Field(default_factory=uuid4)
    _result: UUID | None = None

    def execute(self):
        logger.info("CreateSourceNode.execute()")
        source = usecases.create_node()
        self._result = source.uuid

    def parse_new_events(self) -> list[Event]:
        return []
