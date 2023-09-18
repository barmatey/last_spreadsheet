from uuid import UUID

from spread.source.entity import Source
from spread.source.node import SourceNode
from spread.source.repository import SourceNodeRepo


def create_node() -> SourceNode:
    source = Source()
    node = SourceNode(source)
    repo = SourceNodeRepo()
    repo.add(node)
    return node


def get_node_by_id(uuid: UUID) -> SourceNode:
    repo = SourceNodeRepo()
    node = repo.get_by_id(uuid)
    return node


def save_node(data: SourceNode):
    repo = SourceNodeRepo()
    repo.update(data)
