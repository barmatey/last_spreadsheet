import random
import sys
from copy import deepcopy
from uuid import uuid4, UUID

import pandas as pd
from loguru import logger
#
# logger.remove(0)
# logger.add(sys.stderr, level="INFO")
from spread.formula.repository import FormulaNodeRepo
from spread.sheet.commands import CreatePlanItemsNode, CreateReportFilters
from spread.source.commands import CreateSourceNode
from spread.source.repository import SourceRepo
from spread.wire.commands import CreateWireNode, UpdateWireNode
from spread.wire.repository import WireNodeRepo
from spreadsheet.cell.bootstrap import CellBootstrap
from spreadsheet.cell.entity import Cell
from spreadsheet.formula.bootstrap import FormulaBootstrap
from spreadsheet.sheet.bootstrap import SheetBootstrap
from spreadsheet.sheet.repository import SheetRepo
from spreadsheet.wire.bootstrap import WireBootstrap
from spreadsheet.wire.entity import Wire
from spread.source import usecase as source_usecase


def print_table():
    cell_repo = CellBootstrap().get_repo()
    sheet_repo: SheetRepo = SheetBootstrap().get_repo()

    sheet = sheet_repo.get_all()[0]
    cells = cell_repo.get_filtred({"sheet_id": sheet.uuid})
    size = sheet.size

    # cells = [c.model_copy(deep=True) for c in cells]
    # table = []
    # for i in range(0, size[0]):
    #     row = []
    #     for j in range(0, size[1]):
    #         index = i * size[1] + j
    #         row.append(cells[index].value)
    #     table.append(row)
    # df = pd.DataFrame(table)
    # print(df.to_string())
    #
    # print()
    # print()

    sheet = sheet_repo.get_all()[1]
    cells = cell_repo.get_filtred({"sheet_id": sheet.uuid})
    size = sheet.size

    cells = [c.model_copy(deep=True) for c in cells]
    table = []
    for i in range(0, size[0]):
        row = []
        for j in range(0, size[1]):
            index = i * size[1] + j
            row.append(cells[index].value)
        table.append(row)
    df = pd.DataFrame(table)
    print(df.to_string())


def create_wires(source_id: UUID) -> list[UUID]:
    commands = []
    for i in range(0, 4):
        commands.append(
            CreateWireNode(sender=i, receiver=i + 3, sub1=str(random.random()), amount=random.random(), source_id=source_id)
        )
    results = []
    for cmd in commands:
        cmd.execute()
        results.append(cmd.result())

    return results


def foo():
    formula_repo: FormulaNodeRepo = FormulaNodeRepo()

    cmd = CreateSourceNode()
    cmd.execute()
    source_node_id = cmd.result()

    wire_ids = create_wires(source_node_id)
    wire_id = wire_ids[0]

    cmd = CreatePlanItemsNode(source_id=source_node_id, ccols=['sender', 'sub1'])
    cmd.execute()
    plan_items_id = cmd.result()

    cmd = CreateReportFilters(plan_items_uuid=plan_items_id)
    cmd.execute()

    cmd = UpdateWireNode(uuid=wire_id, sender=5452)
    cmd.execute()

    logger.success(f"plan_items_subs: {formula_repo.get_by_id(plan_items_id)._subs}")
    for sub in formula_repo.get_by_id(plan_items_id)._subs:
        logger.success(f"filter_by: {sub._value.filter_by}")


if __name__ == '__main__':
    # print_hi()
    foo()
