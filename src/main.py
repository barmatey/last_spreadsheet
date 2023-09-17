import sys
from uuid import uuid4

import pandas as pd
from loguru import logger
#
# logger.remove(0)
# logger.add(sys.stderr, level="INFO")
from spread.formula.repository import FormulaRepo
from spread.sheet.commands import CreateGroupSheet
from spread.source.commands import CreateSource
from spread.source.repository import SourceRepo
from spread.wire.commands import CreateWire, UpdateWire
from spread.wire.repository import WireRepo
from spreadsheet.cell.bootstrap import CellBootstrap
from spreadsheet.cell.entity import Cell
from spreadsheet.formula.bootstrap import FormulaBootstrap
from spreadsheet.sheet.bootstrap import SheetBootstrap
from spreadsheet.sheet.repository import SheetRepo
from spreadsheet.wire.bootstrap import WireBootstrap
from spreadsheet.wire.entity import Wire


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


def print_hi():
    cmd = CreateSource()
    cmd.execute()
    source_id = cmd.result()

    cmd = CreateWire(sender=1, sub1='OS', receiver=2, amount=111, source_id=source_id)
    cmd.execute()
    wire_id = cmd.result()

    wire_repo: WireRepo = WireRepo()
    source_repo: SourceRepo = SourceRepo()
    formula_repo: FormulaRepo = FormulaRepo()

    cmd = UpdateWire(uuid=wire_id, sender=123)
    cmd.execute()

    cmd = CreateGroupSheet(source_id=source_id, ccols=['sender', 'sub1'])
    cmd.execute()

    plan = formula_repo.get_by_id(cmd.result())
    print(plan.uniques)


if __name__ == '__main__':
    print_hi()
