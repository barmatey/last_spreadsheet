from uuid import UUID

from helpers.decorators import singleton
from spread.wire.model import Wire


@singleton
class WireRepo:
    def __init__(self):
        self._data = {}

    def add(self, data: Wire):
        self._data[data.uuid] = data

    def update(self, data: Wire):
        if self._data.get(data.uuid) is None:
            raise LookupError
        self._data[data.uuid] = data

    def get_by_id(self, uuid: UUID) -> Wire:
        return self._data[uuid]

