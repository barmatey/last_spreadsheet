from uuid import UUID

from spread.abstract.node import MessageBus
from spread.source.entity import Source, SourceNode
from spread.source.repository import SourceNodeRepo


class CreateNode:
    def __init__(self, repo: SourceNodeRepo, messagebus: MessageBus):
        self._repo = repo
        self._msgbus = messagebus

    def execute(self) -> SourceNode:
        value = Source()
        node = SourceNode(value, self._msgbus, set())
        SourceNodeRepo().add(node)
        return node


def get_node_by_id(uuid: UUID) -> SourceNode:
    repo = SourceNodeRepo()
    node = repo.get_by_id(uuid)
    return node


def save_node(data: SourceNode):
    repo = SourceNodeRepo()
    repo.update(data)
