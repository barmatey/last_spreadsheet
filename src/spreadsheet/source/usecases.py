from uuid import UUID

from spreadsheet.source.entity import SourceNode, Source


def create_node() -> SourceNode:
    node = SourceNode(value=Source())
    return node


def get_node_by_id(uuid: UUID) -> SourceNode:
    raise NotImplemented


def save_node(node: SourceNode):
    raise NotImplemented
