from loguru import logger

from .entity import TestSourceEvent
from . import usecases
from .repository import SourceNodeRepo


class TestSourceEventHandler:
    def __init__(self, repo: SourceNodeRepo = SourceNodeRepo()):
        self._repo = repo

    def handle(self, event: TestSourceEvent):
        logger.debug("TestSourceEventHandler")
        usecases.RemoveNode(event.node, self._repo).execute()
