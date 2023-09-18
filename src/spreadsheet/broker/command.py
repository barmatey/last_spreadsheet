from abc import abstractmethod
from spreadsheet.abstract.pydantic_model import PydanticModel
from spreadsheet.broker.event import Event


class Command(PydanticModel):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def parse_new_events(self) -> list[Event]:
        raise NotImplemented
