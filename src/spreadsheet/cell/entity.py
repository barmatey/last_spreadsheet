from uuid import UUID, uuid4

from pydantic import BaseModel, Field, ConfigDict

from spreadsheet.abstract.cell_value import CellValue
from spreadsheet.abstract.pubsub import Pubsub


class Cell(BaseModel):
    index: tuple
    value: CellValue
    sheet_id: UUID
    subs: list[Pubsub] = Field(default_factory=list)
    uuid: UUID = Field(default_factory=uuid4)

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def partial_copy(self):
        return self.__class__(
            index=self.index,
            value=self.value,
            sheet_id=self.sheet_id,
            subs=self.subs.copy(),
            uuid=self.uuid,
        )
