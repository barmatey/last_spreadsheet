from uuid import UUID

import helpers.decorators
from spreadsheet.abstract.pubsub import Pubsub
from .entity import Wire
from .repository import WireRepo
from ..abstract.cell_value import CellTable


class WireCrudUsecase:
    def __init__(self, repo: WireRepo):
        self._repo = repo

    def create(self) -> Wire:
        raise NotImplemented

    def get_by_id(self) -> Wire:
        raise NotImplemented

    def get_filtred(self, filter_by: dict, order_by: dict = None, asc: bool = True) -> list[Wire]:
        return self._repo.get_filtred(filter_by, order_by, asc)

    def update(self, entity: Wire):
        raise NotImplemented


class UpdateWire:
    def __init__(self, repo: WireRepo):
        self._repo = repo
        self._old_wire: Wire | None = None
        self._new_wire: Wire | None = None

    def load_entity_by_id(self, uuid: UUID) -> 'UpdateWire':
        self._old_wire = self._repo.get_by_id(uuid)
        self._new_wire = self._old_wire.model_copy()
        return self

    def update(self, data: dict) -> 'UpdateWire':
        for key, value in data.items():
            self._new_wire.__setattr__(key, value)
        self._repo.update(self._new_wire)
        return self

    def notify_subscribers(self):
        subs = self._old_wire.subs
        for sub in subs:
            sub.on_update(self._old_wire, self._new_wire)
        for sub in subs:
            sub.on_complete()


class WirePubsub(Pubsub):
    def __init__(self, wires: Wire | list[Wire], repo: WireRepo):
        self._repo = repo
        self._wires = wires if isinstance(wires, list) else [wires]

    def on_before_start(self):
        pass

    def get_entity(self):
        raise NotImplemented

    def notify(self):
        for wire in self._wires:
            for sub in wire.subs:
                print(f"I need to update: {sub}")

    # todo NEED TO OPTIMIZE
    def subscribe(self, subs: Pubsub | list[Pubsub]):
        if not isinstance(subs, list):
            subs = [subs]
        for wire in self._wires:
            for sub in subs:
                wire.subs.append(sub)
                self._repo.update(wire)
                sub.on_before_start()
                sub.on_subscribe(wire)
                sub.on_complete()

    def on_subscribe(self, data):
        raise NotImplemented

    def on_update(self, old_data: CellTable, new_data: CellTable):
        raise NotImplemented

    def on_complete(self):
        raise NotImplemented
