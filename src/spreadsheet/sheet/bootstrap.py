from src.helpers.decorators import singleton
from .repository import SheetRepo, SheetRepoFake


@singleton
class SheetBootstrap:
    def __init__(self, repo: SheetRepo = SheetRepoFake()):
        self._repo = repo

    def get_repo(self) -> SheetRepo:
        return self._repo
