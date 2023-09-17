from uuid import UUID, uuid4

from loguru import logger
from pydantic import Field

from spread.abstract.command import Command
from spread.source.model import Source
from spread.source.repository import SourceRepo


class CreateSource(Command):
    uuid: UUID = Field(default_factory=uuid4)
    _result: UUID | None = None

    def execute(self):
        logger.info("CreateSource.execute()")
        source_repo = SourceRepo()
        source = Source()
        source_repo.add(source)
        self._result = source.uuid

    def result(self) -> UUID:
        if self._result is None:
            raise Exception
        return self._result
