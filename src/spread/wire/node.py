from uuid import UUID, uuid4

from loguru import logger

from spread.abstract.pubsub import Pubsub, Subscriber
from spread.abstract.pydantic_model import PydanticModel
from spread.wire.entity import Wire


class WireNode(Pubsub):
    def __init__(self, value: Wire, subs: list[Subscriber] = None, uuid: UUID = None):
        self._value = value
        self._old_value = None
        self._subs = subs if subs is not None else []
        self.uuid = uuid if uuid is not None else uuid4()
    
    def set_entity_fields(self, data: dict):
        self.on_before_start()
        for key, value in data.items():
            self._value.__setattr__(key, value)
        self.on_complete()
    
    def on_before_start(self):
        self._old_value = self._value.model_copy(deep=True)

    def on_subscribe(self, data: PydanticModel):
        raise NotImplemented

    def on_unsubscribe(self):
        raise NotImplemented

    def on_update(self, _old_data: PydanticModel, new_data: PydanticModel):
        if not isinstance(new_data, Wire):
            raise TypeError
        self._value = new_data

    def on_complete(self):
        logger.debug(f"WireNode.on_complete() => notify {len(self._subs)} subs")
        self.notify()

    def notify(self):
        for sub in self._subs:
            sub.on_before_start()
            sub.on_update(self._old_value, self._value)
            sub.on_complete()

    def subscribe(self, subs: list[Subscriber]):
        logger.debug(f"WireNode.subscribe({subs})")
        for sub in subs:
            sub.on_before_start()
            sub.on_subscribe(self._value)
            sub.on_complete()
            self._subs.append(sub)

    def unsubscribe(self, subs: list[Subscriber]):
        raise NotImplemented
