from uuid import UUID

from helpers.decorators import singleton
from spread.wire.node import WireNode


@singleton
class WireNodeRepo:
    def __init__(self):
        self._data = {}

    def add(self, data: WireNode):
        self._data[data.uuid] = data

    def update(self, data: WireNode):
        if self._data.get(data.uuid) is None:
            raise LookupError
        self._data[data.uuid] = data

    def get_by_id(self, uuid: UUID) -> WireNode:
        return self._data[uuid]

