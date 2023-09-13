from abc import abstractmethod
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class Command(BaseModel):
    uuid: UUID
    model_config = ConfigDict(arbitrary_types_allowed=True)

    @abstractmethod
    def execute(self):
        raise NotImplemented
