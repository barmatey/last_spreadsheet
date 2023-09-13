from uuid import UUID, uuid4

from pydantic import Field

from spreadsheet.abstract.command import Command
from spreadsheet.formula.plan_items import PlanItems, PlanItemsPubsubUsecase
from spreadsheet.formula.sourted_table import SortedTable, SortedTablePubsubUsecase
from spreadsheet.wire.bootstrap import WireBootstrap, WireUniquesUsecase
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
        plan_items = PlanItems()
        formula_repo.add(plan_items)
        plan_items_pubsub = PlanItemsPubsubUsecase(plan_items, formula_repo)

        # Subscribe plan items on wires
        WireUniquesUsecase(
            wires=wire_repo.get_filtred({"source_id": self.source_id}),
            ccols=self.ccols,
            repo=wire_repo).subscribe(plan_items_pubsub)

        # Create SortedTable
        sorted_table = SortedTable()
        formula_repo.add(sorted_table)
        sorted_table_pubsub = SortedTablePubsubUsecase(sorted_table, formula_repo)

        # Subscribe SortedTable on PlanItems
        plan_items_pubsub.subscribe(sorted_table_pubsub)

        print(formula_repo.get_all()[0].utable)
        print(formula_repo.get_all()[1].sorted_data)
