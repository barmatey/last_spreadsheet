from spreadsheet.abstract.pubsub import Pubsub
from .entity import Wire, Ccol
from .repository import WireRepo


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


class WireUniquesUsecase(Pubsub):
    def __init__(self, wires: list[Wire], ccols: list[Ccol], repo: WireRepo):
        self._repo = repo
        self._wires = wires
        self._ccols = ccols

    def subscribe(self, subs: Pubsub | list[Pubsub]):
        if not isinstance(subs, list):
            subs = [subs]
        for wire in self._wires:
            data = [wire.to_table_row(self._ccols)]
            for sub in subs:
                sub.on_next(data)
        for sub in subs:
            sub.on_complete()

    def on_next(self, data):
        raise NotImplemented

    def on_complete(self):
        raise NotImplemented
