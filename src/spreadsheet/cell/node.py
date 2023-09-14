from typing import Union

from spreadsheet.abstract.cell_value import CellTable
from spreadsheet.abstract.pubsub import Pubsub


class CellPubsub(Pubsub):
    def get_entity(self):
        raise NotImplemented

    def notify(self):
        raise NotImplemented

    def subscribe(self, sub: Union['Pubsub', list['Pubsub']]):
        raise NotImplemented

    def on_update(self, old_data: CellTable, new_data: CellTable):
        raise NotImplemented

    def on_subscribe(self, data: CellTable):
        raise NotImplemented

    def on_complete(self):
        raise NotImplemented
