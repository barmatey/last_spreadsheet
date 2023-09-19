from uuid import UUID

from .entity import WireNode, Wire
from .repository import WireNodeRepo


def create_node(data: dict) -> WireNode:
    node = WireNode(value=Wire(**data), subs=[])
    WireNodeRepo().add(node)
    return node


def get_node_by_id(uuid: UUID) -> WireNode:
    return WireNodeRepo().get_by_id(uuid)


def save_node(node: WireNode):
    WireNodeRepo().update(node)
