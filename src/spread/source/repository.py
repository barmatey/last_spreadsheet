from uuid import UUID

from helpers.decorators import singleton
from spread.source.entity import SourceNode


@singleton
class SourceNodeRepo:
    def __init__(self):
        self._data = {}

    def get_all(self) -> list[SourceNode]:
        return list(self._data.values())

    def add(self, data: SourceNode):
        if self._data.get(data.uuid) is not None:
            raise Exception
        self._data[data.uuid] = data

    def update(self, data: SourceNode):
        if self._data.get(data.uuid) is None:
            raise LookupError
        self._data[data.uuid] = data

    def get_by_id(self, uuid: UUID) -> SourceNode:
        return self._data[uuid]

    def remove(self, node: SourceNode):
        del self._data[node.uuid]
