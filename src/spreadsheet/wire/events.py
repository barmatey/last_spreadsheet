from uuid import uuid4

from pydantic import Field

from spreadsheet.abstract.event import Event


class WireUpdated(Event):
    uuid = Field(default_factory=uuid4)

    def handle(self):
        raise NotImplemented
