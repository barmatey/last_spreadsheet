from collections import deque
from uuid import UUID

from loguru import logger

from spread.abstract.command import Command
from spread.abstract.event import Event


def parse_events(results: list) -> set[Event]:
    events = set()
    for result in results:
        events = events | result.parse_events()
    return events


def handle(event: Event):
    pass


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
            self._events.extend(parse_events(results))
            self.results[cmd.uuid] = results

            while self._events:
                event = self._events.popleft()
                logger.error(event)
