from uuid import UUID, uuid4

from loguru import logger
from pydantic import Field

from spread.abstract.command import Command
from . import usecase
from ..abstract.pubsub import Pubsub


class CreateSourceNode(Command):
    uuid: UUID = Field(default_factory=uuid4)

    def execute(self) -> list[Pubsub]:
        logger.info("CreateSourceNode.execute()")
        source = usecase.create_node()
        return [source]
