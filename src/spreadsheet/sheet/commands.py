from uuid import UUID, uuid4

from pydantic import Field

from spreadsheet.abstract.command import Command
from spreadsheet.formula.plan_items import PlanItems, PlanItemsPubsub
from spreadsheet.formula.sorted_table import SortedTable, SortedTablePubsub
from spreadsheet.wire.bootstrap import WireBootstrap, WirePubsub
from spreadsheet.wire.entity import Ccol

from spreadsheet.formula.bootstrap import FormulaBootstrap


class CreateGroupSheet(Command):
    source_id: UUID
    ccols: list[Ccol]
    uuid: UUID = Field(default_factory=uuid4)

    def execute(self):
        # Repositories
        formula_repo = FormulaBootstrap().get_repo()
        wire_repo = WireBootstrap().get_repo()

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
