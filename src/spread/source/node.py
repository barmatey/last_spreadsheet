from uuid import UUID, uuid4

from loguru import logger

from spread.abstract.pubsub import Pubsub, Subscriber
from spread.abstract.pydantic_model import PydanticModel
from spread.source.entity import Source
from spread.wire.entity import Wire


class SourceNode(Pubsub):
    def __init__(self, value: Source, subs: list[Subscriber] = None, uuid: UUID = None):
        self.uuid = uuid if uuid is not None else uuid4()
        self._value = value
        self._subs = subs if subs is not None else []

        self._old_wire = None
        self._new_wire = None

    def __repr__(self):
        return f"SourceNode"

    def on_before_start(self):
        pass

    def on_subscribe(self, data: PydanticModel):
        if isinstance(data, Wire):
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

    def on_complete(self):
        logger.debug(f"SourceNode.on_complete() => notify {len(self._subs)} subs")
        self.notify()

    def notify(self):
        for sub in self._subs:
            sub.on_before_start()
            sub.on_update(self._old_wire, self._new_wire)
            sub.on_complete()

    def subscribe(self, subs: list[Subscriber]):
        logger.debug(f"SourceNode.subscribe({subs})")
        for sub in subs:
            sub.on_before_start()
            for wire in self._value.wires:
                sub.on_subscribe(wire)
            sub.on_complete()
            self._subs.append(sub)
