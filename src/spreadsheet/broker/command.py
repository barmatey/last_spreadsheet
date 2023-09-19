from abc import abstractmethod
from uuid import UUID

from spreadsheet.abstract.pydantic_model import PydanticModel
from spreadsheet.broker.event import Event


class Command(PydanticModel):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def get_uuid(self) -> UUID:
        raise NotImplemented

    @abstractmethod
    def get_result(self):
        raise NotImplemented

    @abstractmethod
    def parse_new_events(self) -> list[Event]:
        raise NotImplemented
