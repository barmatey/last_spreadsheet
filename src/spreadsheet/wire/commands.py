from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime

from loguru import logger
from pydantic import Field

from spreadsheet.abstract.command import Command
from spreadsheet.wire.bootstrap import WireBootstrap, WireRepo
from spreadsheet.wire.usecase import UpdateWire as UpdateWireUsecase


class UpdateWire(Command):
    wire_id: UUID
    currency: Optional[str] = None
    date: Optional[datetime] = None
    sender: Optional[float] = None
    receiver: Optional[float] = None
    amount: Optional[float] = None
    sub1: Optional[str] = None
    sub2: Optional[str] = None
    comment: Optional[str] = None
    source_id: Optional[UUID] = None
    uuid: UUID = Field(default_factory=uuid4)

    def execute(self):
        logger.info("UpdateWire.execute()")
        wire_repo: WireRepo = WireBootstrap().get_repo()
        data = self.model_dump(exclude_none=True, exclude={"uuid", "wire_id"})
        UpdateWireUsecase(wire_repo).load_entity_by_id(self.wire_id).update(data).notify_subscribers()

