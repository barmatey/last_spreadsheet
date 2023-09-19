import typing

from spread.abstract.node import Event, EventHandler
from spread.abstract.pydantic_model import PydanticModel
from spread.source import entity as source_domain, handlers as source_handlers


def handle(event: Event) -> PydanticModel:
    selector: dict[typing.Type[Event], typing.Type[EventHandler]] = {
        source_domain.TestSourceEvent: source_handlers.TestSourceEventHandler,
    }
    handler = selector[type(event)]
    result = handler().handle(event)
    return result
