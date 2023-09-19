from abc import abstractmethod
from uuid import UUID

from spread.abstract.pubsub import Pubsub
from spread.abstract.pydantic_model import PydanticModel


class Command(PydanticModel):
    uuid: UUID

    @abstractmethod
    def execute(self) -> list[Pubsub]:
        raise NotImplemented
