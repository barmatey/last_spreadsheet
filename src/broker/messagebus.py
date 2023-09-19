from collections import deque
from uuid import UUID

from loguru import logger

from helpers.decorators import singleton
from spread.abstract.command import Command
from spread.abstract.event import Event
from .handler import handle


@singleton
class MessageBus:
    def __init__(self):
        self._events: deque[Event] = deque()
        self._commands: deque[Command] = deque()
        self.results: dict[UUID, list] = {}

    def push_command(self, cmd: Command):
        self._commands.append(cmd)

    def push_event(self, event: Event):
        self._events.append(event)

    def run(self):
        while self._commands:
            cmd = self._commands.popleft()
            results = cmd.execute()
            self.results[cmd.uuid] = results

            while self._events:
                event = self._events.popleft()
                handle(event)
