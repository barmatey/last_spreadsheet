import typing
from datetime import datetime
from uuid import UUID, uuid4

from loguru import logger
from pydantic import Field

from spread.abstract.command import Command
from spread.abstract.pubsub import Subscriber
from spread.source.node import SourceNode
from spread.source.repository import SourceRepo
from spread.wire.model import Wire
from spread.wire.node import WireNode
from spread.wire.repository import WireRepo


class CreateWire(Command):
    source_id: UUID
    sender: float
    receiver: float
    amount: float
    sub1: str = ""
    sub2: str = ""
    comment: str = ""
    currency: str = "RU"
    date: datetime = Field(default_factory=datetime.now)
    subs: list[Subscriber] = Field(default_factory=list)
    uuid: UUID = Field(default_factory=uuid4)
    _result: UUID | None = None

    def execute(self):
        logger.info("CreateWire.execute()")
        source_repo = SourceRepo()
        source = source_repo.get_by_id(self.source_id)
        source_node = SourceNode(source)

        wire_repo: WireRepo = WireRepo()
        wire = Wire(**self.model_dump(exclude={"_result", "source_id"}))
        wire_repo.add(wire)
        wire_node = WireNode(wire)
        wire_node.subscribe([source_node])

        self._result = wire.uuid

    def result(self):
        if self._result is None:
            raise Exception
        return self._result


class UpdateWire(Command):
    uuid: UUID
    sender: typing.Optional[float] = None
    receiver: typing.Optional[float] = None
    amount: typing.Optional[float] = None
    sub1: typing.Optional[str] = None
    sub2: typing.Optional[str] = None
    comment: typing.Optional[str] = None
    currency: typing.Optional[str] = None
    date: typing.Optional[datetime] = None
    _result: Wire | None = None

    def execute(self):
        logger.info("UpdateWire.execute()")
        wire_repo: WireRepo = WireRepo()
        target_wire = wire_repo.get_by_id(self.uuid)
        new_wire = target_wire.partial_copy()
        wire_node = WireNode(target_wire)

        for key, value in self.model_dump(exclude_none=True).items():
            new_wire.__setattr__(key, value)
        wire_node.on_before_start()
        wire_node.on_update(target_wire, new_wire)
        wire_node.on_complete()

    def result(self):
        return None
