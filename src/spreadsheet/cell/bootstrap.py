from src.helpers.decorators import singleton
from .repository import CellRepo, CellRepoFake


@singleton
class CellBootstrap:
    def __init__(self, repo: CellRepo = CellRepoFake()):
        self._repo = repo

    def get_repo(self) -> CellRepo:
        return self._repo

