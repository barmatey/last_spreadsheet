from uuid import UUID, uuid4

from pydantic import Field

from spread.abstract.pydantic_model import PydanticModel
from spread.wire.entity import Wire


class Source(PydanticModel):
    wires: list[Wire] = Field(default_factory=list)
    uuid: UUID = Field(default_factory=uuid4)
