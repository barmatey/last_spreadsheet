from abc import ABC, abstractmethod
from pathlib import Path
from uuid import UUID, uuid4

import pandas as pd
from loguru import logger

from src.spreadsheet.wire.entity import Wire


class WireRepo(ABC):
    @abstractmethod
    def add(self, wire: Wire):
        raise NotImplemented

    @abstractmethod
    def get_all(self) -> list[Wire]:
        raise NotImplemented

    @abstractmethod
    def get_by_id(self, uuid: UUID) -> Wire:
        raise NotImplemented

    @abstractmethod
    def get_by_source_id(self, uuid: UUID) -> list[Wire]:
        raise NotImplemented

    @abstractmethod
    def get_filtred(self, filter_by: dict, order_by: dict = None, asc: bool = True) -> list[Wire]:
        raise NotImplemented

    @abstractmethod
    def update(self, wire: Wire):
        raise NotImplemented


class WireRepoFake(WireRepo):
    def __init__(self):
        path = Path("D:/facc_sheet/tests/files/sarmat.csv")
        df = pd.read_csv(path).head(100)
        df['date'] = pd.to_datetime(df['date'])
        df['amount'] = df['debit'] - df['credit']
        df['currency'] = 'rub'
        df['source_id'] = uuid4()

        df = df[['date', 'sender', 'receiver', 'sub1', 'sub2', 'comment', 'currency', 'amount', 'source_id']]
        result = [
            Wire(**record)
            for record in df.to_dict(orient='records')
        ]
        self._wires = result

    def add(self, wire: Wire):
        self._wires.append(wire)

    def get_all(self) -> list[Wire]:
        return self._wires

    def get_by_id(self, uuid: UUID) -> Wire:
        return list(filter(lambda x: x.uuid == uuid, self._wires)).pop()

    def get_by_source_id(self, source_uuid: UUID) -> list[Wire]:
        return self._wires

    def get_filtred(self, filter_by: dict, order_by: dict = None, asc: bool = True) -> list[Wire]:
        result: list[Wire] = []
        for wire in self._wires:
            for key, value in filter_by.items():
                if wire.__getattribute__(key) != value:
                    break
            result.append(wire)
        return result

    def update(self, wire: Wire):
        for i, item in enumerate(self._wires):
            if item.uuid == wire.uuid:
                self._wires[i] = wire
                return
        raise LookupError
