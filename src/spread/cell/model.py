import typing
from uuid import UUID, uuid4

from pydantic import Field

from spread.abstract.pubsub import Subscriber
from spread.abstract.pydantic_model import PydanticModel

CellValue = typing.Union[int, float, str, None]


class Cell(PydanticModel):
    value: CellValue
    index: tuple[int, int]
    subs: list[Subscriber] = Field(default_factory=list)
    uuid: UUID = Field(default_factory=uuid4)

    def partial_copy(self):
        return self.__class__(
            value=self.value,
            index=self.index,
            subs=self.subs.copy(),
            uuid=self.uuid,
        )
