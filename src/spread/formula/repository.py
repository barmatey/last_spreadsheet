from uuid import UUID

from loguru import logger

from helpers.decorators import singleton
from spread.formula.node import FormulaNode


@singleton
class FormulaNodeRepo:
    def __init__(self):
        self._data = {}

    def add(self, formula: FormulaNode):
        if self._data.get(formula.uuid) is not None:
            raise Exception
        self._data[formula.uuid] = formula

    def update(self, formula: FormulaNode):
        if self._data.get(formula.uuid) is None:
            raise LookupError
        self._data[formula.uuid] = formula

    def get_by_id(self, uuid: UUID) -> FormulaNode:
        return self._data[uuid]

    def get_all(self) -> list[FormulaNode]:
        return list(self._data.values())

    def destroy_by_id(self, uuid: UUID):
        del self._data[uuid]
