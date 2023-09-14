from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Sheet(BaseModel):
    title: str
    uuid: UUID = Field(default_factory=uuid4)
