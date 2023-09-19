import typing
from datetime import datetime
from uuid import UUID, uuid4

from loguru import logger
from pydantic import Field

from spread.abstract.node import Node
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


class WireNode(Node):
    def on_subscribe(self, data: PydanticModel):
        raise NotImplemented

    def on_update(self, old_data: PydanticModel, new_data: PydanticModel):
        if not isinstance(new_data, Wire):
            raise TypeError
        self._value = new_data

    def on_unsubscribe(self, data: PydanticModel):
        raise NotImplemented

    def on_complete(self):
        logger.debug(f"WireNode.on_complete() => notify {len(self._subs)} subs")
        self.notify()
