from uuid import UUID, uuid4

from loguru import logger
from pydantic import Field

from spread.abstract.command import Command
from . import usecase


class CreateSourceNode(Command):
    uuid: UUID = Field(default_factory=uuid4)
    _result: UUID | None = None

    def execute(self):
        logger.info("CreateSourceNode.execute()")
        source = usecase.create_node()
        self._result = source.uuid

    def result(self) -> UUID:
        if self._result is None:
            raise Exception
        return self._result
