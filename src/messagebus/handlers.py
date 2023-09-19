from spread.abstract.node import Event
from spread.abstract.pydantic_model import PydanticModel
from spread.source import events as source_events, usecase as source_handlers


def handle(event: Event) -> PydanticModel:
    selector = {
        source_events.TestSourceEvent: source_handlers.RemoveNode,
    }
    handler = selector[type(event)]
    result = handler(event)
