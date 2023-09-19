from collections import deque

from .command import Command
from .event import Event
from .handler import Handler
from ..abstract.pubsub import Subscriber


def get_event_handler(sub: Subscriber, event: Event) -> Handler:
    pass


class MessageBus:
    def __init__(self):
        self._event_queue: deque[Event] = deque()
        self._command_queue: deque[Command] = deque()
        self.results = {}

    def push_command(self, cmd: Command):
        self._command_queue.append(cmd)

    def run(self):
        while self._command_queue:
            cmd = self._command_queue.popleft()
            cmd.execute()
            self._event_queue.extend(cmd.parse_new_events())
            self.results[cmd.get_uuid()] = cmd.get_result()

            while self._event_queue:
                event = self._event_queue.popleft()
                for sub in event.pub.get_subs():
                    handler = get_event_handler(sub, event)
                    handler.handle()
                    self._event_queue.extend(handler.parse_new_events())
