from abc import abstractmethod
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class Event(BaseModel):
    uuid: UUID
    model_config = ConfigDict(arbitrary_types_allowed=True)

    @abstractmethod
    def handle(self):
        raise NotImplemented
