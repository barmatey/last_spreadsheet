from uuid import UUID

from loguru import logger

from helpers.decorators import singleton
from spread.formula.model import Formula


@singleton
class FormulaRepo:
    def __init__(self):
        self._data = {}

    def add(self, formula: Formula):
        if self._data.get(formula.uuid) is not None:
            raise Exception
        self._data[formula.uuid] = formula

    def update(self, formula: Formula):
        if self._data.get(formula.uuid) is None:
            raise LookupError
        self._data[formula.uuid] = formula

    def get_by_id(self, uuid: UUID) -> Formula:
        return self._data[uuid]

    def get_all(self) -> list[Formula]:
        return list(self._data.values())
