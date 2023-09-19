from uuid import UUID, uuid4

from loguru import logger
from pydantic import Field

from spreadsheet.abstract.command import Command
from spreadsheet.abstract.event import Event
from . import usecases


class CreateSourceNode(Command):
    uuid: UUID = Field(default_factory=uuid4)
    _result: UUID | None = None

    def execute(self):
        logger.info("CreateSourceNode.execute()")
        source = usecases.create_node()
        self._result = source.uuid

    def get_uuid(self) -> UUID:
        return self.uuid

    def get_result(self):
        return self._result

    def parse_new_events(self) -> list[Event]:
        return []
