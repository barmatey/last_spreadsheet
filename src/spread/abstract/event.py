from uuid import UUID

from spread.abstract.pydantic_model import PydanticModel


class Event(PydanticModel):
    uuid: UUID
