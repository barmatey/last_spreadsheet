from uuid import UUID

from pydantic import BaseModel, ConfigDict


class Formula(BaseModel):
    uuid: UUID
    model_config = ConfigDict(arbitrary_types_allowed=True)
