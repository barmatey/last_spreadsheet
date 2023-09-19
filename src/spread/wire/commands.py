import typing
from datetime import datetime
from uuid import UUID, uuid4

from loguru import logger
from pydantic import Field

from spread.abstract.command import Command
from spread.source import usecase as source_usecase
from spread.wire import usecase as wire_usecase


class CreateWireNode(Command):
    source_id: UUID
    sender: float
    receiver: float
    amount: float
    sub1: str = ""
    sub2: str = ""
    comment: str = ""
    currency: str = "RU"
    date: datetime = Field(default_factory=datetime.now)
    uuid: UUID = Field(default_factory=uuid4)
    _result: UUID | None = None

    def execute(self):
        logger.info("CreateWireNode.execute()")
        # Execute
        source_node = source_usecase.get_node_by_id(self.source_id)
        wire_node = wire_usecase.create_node(**self.model_dump(exclude={"_result", "source_id"}))
        wire_node.subscribe([source_node])

        # Save
        source_usecase.save_node(source_node)  # Should I do this?
        wire_usecase.save_node(wire_node)

        # Result
        self._result = wire_node.uuid

    def result(self):
        if self._result is None:
            raise Exception
        return self._result


class UpdateWireNode(Command):
    uuid: UUID
    sender: typing.Optional[float] = None
    receiver: typing.Optional[float] = None
    amount: typing.Optional[float] = None
    sub1: typing.Optional[str] = None
    sub2: typing.Optional[str] = None
    comment: typing.Optional[str] = None
    currency: typing.Optional[str] = None
    date: typing.Optional[datetime] = None
    _result: None = None

    def execute(self):
        logger.info("UpdateWire.execute()")
        wire_node = wire_usecase.get_node_by_id(self.uuid)
        wire_node.set_entity_fields(self.model_dump(exclude_none=True, exclude={"_result"}))
        wire_usecase.save_node(wire_node)

    def result(self):
        return None
