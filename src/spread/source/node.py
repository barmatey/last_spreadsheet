from loguru import logger

from spread.abstract.pubsub import Pubsub, Subscriber
from spread.abstract.pydantic_model import PydanticModel
from spread.source.model import Source
from spread.wire.model import Wire
from spread.source.repository import SourceRepo


class SourceNode(Pubsub):
    def __init__(self, source: Source):
        self._source = source
        self._source_repo = SourceRepo()

        self._old_wire = None
        self._new_wire = None

    def on_before_start(self):
        pass

    def on_subscribe(self, data: PydanticModel):
        if isinstance(data, Wire):
            self._source.wires.append(data)

    def on_update(self, old_data: PydanticModel, new_data: PydanticModel):
        if isinstance(old_data, Wire) and isinstance(new_data, Wire):
            self._old_wire = old_data
            self._new_wire = new_data
            for i, wire in enumerate(self._source.wires):
                if wire.uuid == new_data.uuid:
                    self._source.wires[i] = new_data
                    return
            raise LookupError
        raise TypeError

    def on_complete(self):
        logger.debug(f"SourceNode.on_complete() => notify {len(self._source.subs)} subs")
        self._source_repo.update(self._source)
        self.notify()

    def notify(self):
        for sub in self._source.subs:
            sub.on_before_start()
            sub.on_update(self._old_wire, self._new_wire)
            sub.on_complete()

    def subscribe(self, subs: list[Subscriber]):
        logger.debug(f"SourceNode.subscribe({subs})")
        for sub in subs:
            sub.on_before_start()
            for wire in self._source.wires:
                sub.on_subscribe(wire)
            sub.on_complete()
            self._source.subs.append(sub)
        self._source_repo.update(self._source)
