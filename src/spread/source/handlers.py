from loguru import logger

from .entity import TestSourceEvent
from . import usecases
from .repository import SourceNodeRepo
from ..abstract.node import EventHandler


class TestSourceEventHandler(EventHandler):
    def __init__(self, repo: SourceNodeRepo = SourceNodeRepo()):
        self._repo = repo

    def handle(self, event: TestSourceEvent):
        logger.debug("TestSourceEventHandler")
        usecases.RemoveNode(event.node, self._repo).execute()


class SourceNodeUpdated(EventHandler):
    def __init__(self, repo: SourceNodeRepo = SourceNodeRepo()):
        self._repo = repo

    def handle(self, event: TestSourceEvent):
        logger.debug("SourceNodeUpdated")
        for sub in event.node._subs:
            sub.on_update()
            sub.on_complete()

