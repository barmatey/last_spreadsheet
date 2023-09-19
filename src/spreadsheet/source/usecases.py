from uuid import UUID

from spreadsheet.source.entity import SourceNode, Source
from spreadsheet.source.repository import SourceNodeRepo


def create_node() -> SourceNode:
    node = SourceNode(value=Source())
    SourceNodeRepo().add(node)
    return node


def get_node_by_id(uuid: UUID) -> SourceNode:
    return SourceNodeRepo().get_by_id(uuid)


def save_node(node: SourceNode):
    SourceNodeRepo().update(node)
