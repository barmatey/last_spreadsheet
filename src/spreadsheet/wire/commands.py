from copy import copy
from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime

from loguru import logger
from pydantic import Field

from spreadsheet.abstract.command import Command
from spreadsheet.wire.bootstrap import WireBootstrap, WireRepo
from spreadsheet.wire.usecase import UpdateWireSubs


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
        logger.debug("UpdateWire.execute()")
        wire_repo: WireRepo = WireBootstrap().get_repo()
        wire = wire_repo.get_by_id(self.wire_id)
        old_wire = copy(wire)

        data = self.model_dump(exclude_none=True, exclude={"uuid", "wire_id"})
        for key, value in data.items():
            wire.__setattr__(key, value)
        wire_repo.update(wire)

        UpdateWireSubs(old_wire, wire).notify()
