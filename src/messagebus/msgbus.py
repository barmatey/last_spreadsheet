from collections import deque
from uuid import UUID

from loguru import logger

from helpers.decorators import singleton
from spread.abstract.node import MessageBus, Command, Event
from spread.abstract.pydantic_model import PydanticModel

from spread.source import usecase

from .handlers import handle


@singleton
class SourceMsgbus(MessageBus):
    def __init__(self):
        self._commands: deque[Command] = deque()
        self._events: deque[Event] = deque()
        self.results: dict[UUID, PydanticModel] = {}

    def push_command(self, cmd: Command):
        self._commands.append(cmd)

    def push_event(self, event: Event):
        self._events.append(event)

    def run(self):
        while self._commands:
            cmd = self._commands.popleft()
            self.results[cmd.uuid] = cmd.execute()

            while self._events:
                event = self._events.popleft()
                handle(event)
