from spread.abstract.pubsub import Pubsub, Subscriber
from spread.abstract.pydantic_model import PydanticModel
from spread.cell.model import Cell
from spread.cell.repository import CellRepo


class CellNode(Pubsub):
    def __init__(self, cell: Cell):
        super().__init__()
        self._old_cell = cell
        self._cell = cell.partial_copy()
        self._cell_repo = CellRepo()

    def on_before_start(self):
        self._old_cell = self._cell.partial_copy()

    def on_subscribe(self, data: PydanticModel):
        if isinstance(data, Cell):
            self._cell.value = data.value
        else:
            raise NotImplemented

    def on_update(self, old_data: PydanticModel, new_data: PydanticModel):
        if isinstance(new_data, Cell):
            self._cell.value = new_data.value
        else:
            raise NotImplemented

    def on_complete(self):
        self._cell_repo.update(self._cell)

    def notify(self):
        for sub in self._cell.subs:
            sub.on_before_start()
            sub.on_update(self._old_cell, self._cell)
            sub.on_complete()

    def subscribe(self, subs: list[Subscriber]):
        for sub in subs:
            sub.on_before_start()
            sub.on_update(self._old_cell, self._cell)
            sub.on_complete()
            self._cell.subs.append(sub)
            self._cell_repo.update(self._cell)

    def unsubscribe(self, subs: list[Subscriber]):
        raise NotImplemented
