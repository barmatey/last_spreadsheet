from uuid import UUID, uuid4

from pydantic import Field

from spreadsheet.abstract.command import Command
from spreadsheet.formula.collection.plan_items import PlanItems, PlanItemsPubsub
from spreadsheet.formula.repository import FormulaRepo
from spreadsheet.formula.collection.sorted_table import SortedTable, SortedTablePubsub
from spreadsheet.sheet.bootstrap import SheetBootstrap
from spreadsheet.sheet.repository import SheetRepo
from spreadsheet.wire.bootstrap import WireBootstrap, WirePubsub
from spreadsheet.wire.entity import Ccol

from spreadsheet.formula.bootstrap import FormulaBootstrap
from spreadsheet.wire.repository import WireRepo


class CreateGroupSheet(Command):
    source_id: UUID
    ccols: list[Ccol]
    uuid: UUID = Field(default_factory=uuid4)

    def execute(self):
        # Repositories
        formula_repo: FormulaRepo = FormulaBootstrap().get_repo()
        wire_repo: WireRepo = WireBootstrap().get_repo()
        sheet_repo: SheetRepo = SheetBootstrap().get_repo()

        # Create PlanItems
        plan_items = PlanItems(ccols=self.ccols)
        formula_repo.add(plan_items)
        plan_items_pubsub = PlanItemsPubsub(plan_items, formula_repo)

        # Subscribe PlanItems on wires
        WirePubsub(
            wires=wire_repo.get_filtred({"source_id": self.source_id}),
            repo=wire_repo).subscribe(plan_items_pubsub)

        # Create SortedTable and subscribe SortedTable on PlanItems
        sorted_table = SortedTable()
        formula_repo.add(sorted_table)
        sorted_table_pubsub = SortedTablePubsub(sorted_table, formula_repo)
        plan_items_pubsub.subscribe(sorted_table_pubsub)

        # Create sheet
        # size = (len(plan_items_pubsub.get_entity().utable), len(plan_items_pubsub.get_entity().utable[0]))
        # (CreateSheet(sheet_repo)
        #  .set_title("main")
        #  .set_size(size)
        #  .create()
        #  )
