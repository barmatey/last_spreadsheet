from helpers.decorators import singleton
from spread.cell.model import Cell


@singleton
class CellRepo:
    def add(self, model: Cell):
        pass

    def update(self, model: Cell):
        pass
