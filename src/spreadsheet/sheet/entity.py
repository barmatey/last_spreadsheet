from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Sheet(BaseModel):
    title: str
    size: tuple[int, int]
    uuid: UUID = Field(default_factory=uuid4)

    def partial_copy(self):
        return self.__class__(
            title=self.title,
            size=self.size,
            uuid=self.uuid,
        )
