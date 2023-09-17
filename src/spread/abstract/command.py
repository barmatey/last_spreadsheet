from abc import abstractmethod
from uuid import UUID

from spread.abstract.pydantic_model import PydanticModel


class Command(PydanticModel):
    uuid: UUID

    @abstractmethod
    def execute(self):
        raise NotImplemented

    @abstractmethod
    def result(self):
        raise NotImplemented
