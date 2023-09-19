from collections import deque

from spread.abstract.command import Command
from spread.abstract.event import Event


class MessageBus:
    def __init__(self):
        self._events: deque[Event] = deque()
        self._commands: deque[Command] = deque()
        self.results = {}

    def push_command(self, cmd: Command):
        self._commands.append(cmd)

    def push_event(self, event: Event):
        self._events.append(event)

    def run(self):
        while self._commands:
            cmd = self._commands.popleft()
            cmd.execute()
            self.results[cmd.uuid] = cmd.result()

            while self._events:
                event = self._events.popleft()
