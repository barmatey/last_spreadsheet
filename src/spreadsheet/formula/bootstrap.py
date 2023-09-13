from src.helpers.decorators import singleton
from .repository import FormulaRepo, FormulaRepoFake


@singleton
class FormulaBootstrap:
    def __init__(self, repo: FormulaRepo = FormulaRepoFake()):
        self._repo = repo

    def get_repo(self) -> FormulaRepo:
        return self._repo

