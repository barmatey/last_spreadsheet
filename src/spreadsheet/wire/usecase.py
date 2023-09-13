from typing import Union

from spreadsheet.abstract.pubsub import Pubsub, Publisher
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


class UpdateWireSubs:
    def __init__(self, old_wire: Wire, new_wire: Wire):
        self._old_wire = old_wire
        self._new_wire = new_wire

    def notify(self):
        subs = self._old_wire.subs
        for sub in subs:
            sub.on_update(self._old_wire, self._new_wire)
        for sub in subs:
            sub.on_complete()


class WirePubsub(Pubsub):
    def __init__(self, wires: Wire | list[Wire], repo: WireRepo):
        self._repo = repo
        self._wires = wires if isinstance(wires, list) else [wires]

    def notify(self):
        for wire in self._wires:
            for sub in wire.subs:
                print(f"I need to update: {sub}")

    def subscribe(self, subs: Pubsub | list[Pubsub]):
        if not isinstance(subs, list):
            subs = [subs]
        for wire in self._wires:
            for sub in subs:
                sub.on_subscribe(wire)
                wire.subs.append(sub)
                self._repo.update(wire)
        for sub in subs:
            sub.on_complete()

    def on_subscribe(self, data):
        raise NotImplemented

    def on_update(self, old_data: CellTable, new_data: CellTable):
        raise NotImplemented

    def on_complete(self):
        raise NotImplemented
