from loguru import logger

from spread.abstract.pubsub import Pubsub, Subscriber
from spread.abstract.pydantic_model import PydanticModel
from spread.formula.repository import FormulaRepo
from spread.wire.model import Wire
from spread.wire.repository import WireRepo


class WireNode(Pubsub):
    def __init__(self, model: Wire):
        self._old_model = model
        self._model = model.partial_copy()
        self._wire_repo = WireRepo()

    def on_before_start(self):
        self._old_model = self._model.partial_copy()

    def on_subscribe(self, data: PydanticModel):
        raise NotImplemented

    def on_update(self, old_data: PydanticModel, new_data: PydanticModel):
        if not isinstance(new_data, Wire):
            raise TypeError
        self._model = new_data

    def on_complete(self):
        logger.debug(f"WireNode.on_complete() => notify {len(self._model.subs)} subs")
        self._wire_repo.update(self._model)
        self.notify()

    def notify(self):
        for sub in self._model.subs:
            sub.on_before_start()
            sub.on_update(self._old_model, self._model)
            sub.on_complete()

    def subscribe(self, subs: list[Subscriber]):
        logger.debug(f"WireNode.subscribe({subs})")
        for sub in subs:
            sub.on_before_start()
            sub.on_subscribe(self._model)
            sub.on_complete()
            self._model.subs.append(sub)
        self._wire_repo.update(self._model)
