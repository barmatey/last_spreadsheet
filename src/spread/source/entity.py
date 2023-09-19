from uuid import UUID, uuid4

from loguru import logger
from pydantic import Field

from spread.abstract.node import Node, MessageBus
from spread.abstract.pydantic_model import PydanticModel
from spread.wire.entity import Wire

from . import events


class Source(PydanticModel):
    wires: list[Wire] = Field(default_factory=list)
    uuid: UUID = Field(default_factory=uuid4)


class SourceNode(Node):
    def __init__(self, value: Source, messagebus: MessageBus, subs: set[Node], uuid: UUID = None):
        super().__init__(value, messagebus, subs, uuid)
        self._old_wire = None
        self._new_wire = None

        self._messagebus.push_event(events.TestSourceEvent(node=self))

    def __repr__(self):
        return f"SourceNode"

    def on_before_start(self):
        pass

    def on_subscribe(self, data: PydanticModel):
        if not isinstance(data, Wire):
            raise ValueError
        self._value.wires.append(data)

    def on_update(self, old_data: PydanticModel, new_data: PydanticModel):
        if isinstance(old_data, Wire) and isinstance(new_data, Wire):
            self._old_wire = old_data
            self._new_wire = new_data
            for i, wire in enumerate(self._value.wires):
                if wire.uuid == new_data.uuid:
                    self._value.wires[i] = new_data
                    return
            raise LookupError
        raise TypeError

    def on_unsubscribe(self, data: PydanticModel):
        raise NotImplemented

    def on_complete(self):
        logger.debug(f"SourceNode.on_complete() => notify {len(self._subs)} subs")
        self.notify()

    def subscribe(self, subs: list[Node]):
        logger.debug(f"SourceNode.subscribe({subs})")
        for sub in subs:
            sub.on_before_start()
            for wire in self._value.wires:
                sub.on_subscribe(wire)
            sub.on_complete()
            self._subs.add(sub)
