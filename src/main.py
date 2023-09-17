import sys
from uuid import uuid4

import pandas as pd
from loguru import logger
#
# logger.remove(0)
# logger.add(sys.stderr, level="INFO")


from spreadsheet.cell.bootstrap import CellBootstrap
from spreadsheet.cell.entity import Cell
from spreadsheet.formula.bootstrap import FormulaBootstrap
from spreadsheet.sheet.bootstrap import SheetBootstrap
from spreadsheet.sheet.commands import CreateGroupSheet, CreateReportSheet
from spreadsheet.sheet.repository import SheetRepo
from spreadsheet.wire.bootstrap import WireBootstrap
from spreadsheet.wire.commands import UpdateWire
from spreadsheet.wire.entity import Wire
from spreadsheet.wire.repository import WireRepo


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
    cmd = CreateGroupSheet(source_id=uuid4(), ccols=['sender', 'sub1'])
    cmd.execute()

    sheet_repo: SheetRepo = SheetBootstrap().get_repo()
    group_id = sheet_repo.get_all()[0].uuid
    cmd = CreateReportSheet(source_id=uuid4(), group_sheet_id=group_id, ccols=['sender', 'sub1'])
    cmd.execute()

    wire_repo: WireRepo = WireBootstrap().get_repo()
    old_wire = wire_repo.get_all()[0]

    print_table()
    print()

    cmd = UpdateWire(wire_id=old_wire.uuid, sender=66.1, sub1="сарматтекущий")
    cmd.execute()

    print_table()


if __name__ == '__main__':
    print_hi()
