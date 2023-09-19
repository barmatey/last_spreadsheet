from uuid import UUID

from loguru import logger

from spread.abstract.node import MessageBus
from .entity import Source, SourceNode
from .repository import SourceNodeRepo


class CreateNode:
    def __init__(self, repo: SourceNodeRepo, messagebus: MessageBus):
        self._repo = repo
        self._msgbus = messagebus

    def execute(self) -> SourceNode:
        value = Source()
        node = SourceNode(value, self._msgbus, set())
        SourceNodeRepo().add(node)
        return node


class RemoveNode:
    def __init__(self, node: SourceNode, repo: SourceNodeRepo):
        self._node = node
        self._repo = repo

    def execute(self):
        self._repo.remove(self._node)


def get_node_by_id(uuid: UUID) -> SourceNode:
    repo = SourceNodeRepo()
    node = repo.get_by_id(uuid)
    return node


def save_node(data: SourceNode):
    repo = SourceNodeRepo()
    repo.update(data)
