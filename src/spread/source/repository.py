from uuid import UUID

from helpers.decorators import singleton
from spread.source.model import Source


@singleton
class SourceRepo:
    def __init__(self):
        self._data = {}

    def add(self, data: Source):
        self._data[data.uuid] = data

    def update(self, data: Source):
        if self._data.get(data.uuid) is None:
            raise LookupError
        self._data[data.uuid] = data

    def get_by_id(self, uuid: UUID) -> Source:
        return self._data[uuid]
