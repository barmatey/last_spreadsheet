from uuid import UUID, uuid4

import pandas as pd
from loguru import logger
from pydantic import Field

from spreadsheet.abstract.command import Command
from spreadsheet.cell.bootstrap import CellBootstrap
from spreadsheet.cell.entity import Cell
from spreadsheet.cell.node import CellPubsub
from spreadsheet.cell.repository import CellRepo
from spreadsheet.cell import usecase as cell_usecase
from spreadsheet.formula.collection.plan_items import PlanItems, PlanItemsPubsub
from spreadsheet.formula.repository import FormulaRepo
from spreadsheet.formula.collection.sorted_table import SortedTable, SortedTablePubsub
from spreadsheet.sheet.bootstrap import SheetBootstrap
from spreadsheet.sheet.repository import SheetRepo
from spreadsheet.wire.bootstrap import WireBootstrap, WirePubsub
from spreadsheet.wire.entity import Ccol

from src.spreadsheet.sheet import usecase as sheet_usecase

from spreadsheet.formula.bootstrap import FormulaBootstrap
from spreadsheet.wire.repository import WireRepo


class CreateGroupSheet(Command):
    source_id: UUID
    ccols: list[Ccol]
    uuid: UUID = Field(default_factory=uuid4)

    def execute(self):
        logger.debug("CreateGroupSheet.execute()")

        # Repositories
        formula_repo: FormulaRepo = FormulaBootstrap().get_repo()
        wire_repo: WireRepo = WireBootstrap().get_repo()
        cell_repo: CellRepo = CellBootstrap().get_repo()
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
        size = (len(plan_items_pubsub.get_entity().utable), len(plan_items_pubsub.get_entity().utable[0]))
        sheet_id = uuid4()
        sheet_usecase.CreateSheet(sheet_id, "main", size, sheet_repo, cell_repo).execute()
        target_cell = cell_repo.get_filtred({"sheet_id": sheet_id, "index": (0, 0)})[0]
        cell_pubsub = CellPubsub(target_cell)

        sorted_table_pubsub.subscribe(cell_pubsub)


class CreateReportSheet(Command):
    source_id: UUID
    group_sheet_id: UUID
    uuid: UUID = Field(default_factory=uuid4)

    def execute(self):
        logger.debug(f"CreateReportSheet.execute()")
        # Repositories
        cell_repo: CellRepo = CellBootstrap().get_repo()
        sheet_repo: SheetRepo = SheetBootstrap().get_repo()

        group_sheet = sheet_repo.get_by_id(self.group_sheet_id)
        blank_report_sheet = sheet_usecase.CreateSheet(
            sheet_id=uuid4(),
            title="main",
            size=(group_sheet.size[0], group_sheet.size[1] + 1),
            sheet_repo=sheet_repo,
            cell_repo=cell_repo
        ).execute()

        for i in range(0, group_sheet.size[0]):
            for j in range(0, group_sheet.size[1]):
                from_cell = cell_repo.get_by_index(group_sheet.uuid, (i, j))
                from_cell_pubsub = CellPubsub(from_cell)

                to_cell = cell_repo.get_by_index(blank_report_sheet.uuid, (i, j))
                to_cell_pubsub = CellPubsub(to_cell)

                from_cell_pubsub.subscribe(to_cell_pubsub)
