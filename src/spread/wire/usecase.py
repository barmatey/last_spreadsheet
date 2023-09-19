from datetime import datetime
from uuid import UUID, uuid4

from ..abstract.node import MessageBus
from .entity import Wire, WireNode
from .repository import WireNodeRepo


class CreateNode:
    def __init__(self, data: dict, messagebus: MessageBus, repo: WireNodeRepo):
        self._data = data
        self._repo = repo
        self._messagebus = messagebus

    def execute(self) -> WireNode:
        wire = Wire(**self._data)
        node = WireNode(wire, self._messagebus)
        self._repo.add(node)
        return node


def get_node_by_id(uuid: UUID) -> WireNode:
    repo = WireNodeRepo()
    node = repo.get_by_id(uuid)
    return node


def update_node_value(uuid: UUID, data: dict):
    repo = WireNodeRepo()
    node = repo.get_by_id(uuid)
    node.set_entity_fields(data)


def save_node(data: WireNode):
    repo = WireNodeRepo()
    repo.update(data)
