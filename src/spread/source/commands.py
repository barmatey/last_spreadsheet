from dataclasses import dataclass, field
from uuid import UUID, uuid4

from loguru import logger

from broker.messagebus import MessageBus
from . import usecases
from .repository import SourceNodeRepo
from ..abstract.node import Command
from ..abstract.pydantic_model import PydanticModel


@dataclass
class CreateSourceNode(Command):
    msgbus: MessageBus
    repo: SourceNodeRepo
    uuid: UUID = field(default_factory=uuid4)

    def execute(self) -> PydanticModel:
        node = usecases.CreateNode(self.repo, self.msgbus).execute()
        return node.value
