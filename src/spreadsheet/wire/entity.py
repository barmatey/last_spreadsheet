import typing
from uuid import UUID, uuid4
from datetime import datetime

from pydantic import Field, BaseModel, ConfigDict

from spreadsheet.abstract.cell_value import CellValue
from spreadsheet.abstract.pubsub import Pubsub

Ccol = typing.Literal['currency', 'sender', 'receiver', 'sub1', 'sub2', 'comment']


class Wire(BaseModel):
    currency: str
    date: datetime
    sender: float
    receiver: float
    amount: float
    sub1: str
    sub2: str
    comment: str
    source_id: UUID
    subs: list[Pubsub] = Field(default_factory=list)
    uuid: UUID = Field(default_factory=uuid4)

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def to_table_row(self, ccols: list[Ccol]) -> list[CellValue]:
        return [self.__getattribute__(x) for x in ccols]
