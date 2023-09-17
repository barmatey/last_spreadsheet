from uuid import UUID

from spread.abstract.pydantic_model import PydanticModel


class Formula(PydanticModel):
    uuid: UUID

