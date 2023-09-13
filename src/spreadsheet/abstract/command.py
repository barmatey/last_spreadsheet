from abc import abstractmethod
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class Command(BaseModel):
    uuid: UUID
    next_commands: Optional[list['Command']] = None
    model_config = ConfigDict(arbitrary_types_allowed=True)

    @abstractmethod
    def execute(self):
        raise NotImplemented

    def parse_next_commands(self) -> list['Command']:
        if self.next_commands is None:
            raise ValueError
        commands = self.next_commands
        self.next_commands = []
        return commands
