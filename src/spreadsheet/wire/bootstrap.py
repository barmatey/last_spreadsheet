from spreadsheet.wire.entity import Wire, Ccol
from src.helpers.decorators import singleton
from .repository import WireRepo, WireRepoFake
from .usecase import WireCrudUsecase, WireUniquesUsecase


@singleton
class WireBootstrap:

    def __init__(self):
        self.__repo: WireRepo = WireRepoFake()

    def get_repo(self) -> WireRepo:
        return self.__repo

    def get_crud_usecase(self) -> WireCrudUsecase:
        return WireCrudUsecase(self.__repo)

    def get_wire_uniques_usecase(self, wires: list[Wire], ccols: list[Ccol]) -> WireUniquesUsecase:
        return WireUniquesUsecase(wires, ccols, self.__repo)
