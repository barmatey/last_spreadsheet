from collections import deque
from uuid import UUID

from helpers.decorators import singleton
from spread.abstract.pubsub import Subscriber
from spread.abstract.pydantic_model import PydanticModel
from spread.formula.collection.report_filter.entity import ReportFilterNode
from spread.formula.collection.report_filter.handlers import handle_plan_items_node_updated


class Event(PydanticModel):
    subs: list[Subscriber]


def get_handler(sub: Subscriber):
    if isinstance(sub, ReportFilterNode):
        return handle_plan_items_node_updated


@singleton
class MessageBus:
    def __init__(self):
        self._event_queue: deque[Event] = deque()

    def push_event(self):
        pass

    def run(self):
        while self._event_queue:
            event = self._event_queue.popleft()
            for sub in event.subs:
                handler = get_handler(sub)