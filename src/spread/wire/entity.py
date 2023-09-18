import typing
from datetime import datetime
from uuid import UUID, uuid4

from pydantic import Field

from spread.abstract.pubsub import Subscriber
from spread.abstract.pydantic_model import PydanticModel
from spread.cell.model import CellValue

Ccol = typing.Literal['currency', 'sender', 'receiver', 'sub1', 'sub2', 'comment']


class Wire(PydanticModel):
    currency: str
    date: datetime
    sender: float
    receiver: float
    amount: float
    sub1: str
    sub2: str
    comment: str
    uuid: UUID = Field(default_factory=uuid4)

    def to_table_row(self, ccols: list[Ccol]) -> list[CellValue]:
        return [self.__getattribute__(x) for x in ccols]
