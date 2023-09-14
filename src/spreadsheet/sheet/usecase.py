from .entity import Sheet
from .repository import SheetRepo


class CreateSheet:
    def __init__(self, repo: SheetRepo):
        self._repo = repo
        self._title = ""
        self._size = (300, 20)

    def set_title(self, title: str) -> 'CreateSheet':
        self._title = title
        return self

    def set_size(self, size: tuple[int, int]) -> 'CreateSheet':
        self._size = size
        return self

    def create(self) -> Sheet:
        raise NotImplemented
