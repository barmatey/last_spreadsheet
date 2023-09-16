from copy import deepcopy
from uuid import uuid4

import pandas as pd
from loguru import logger

from spreadsheet.cell.bootstrap import CellBootstrap
from spreadsheet.cell.entity import Cell
from spreadsheet.formula.bootstrap import FormulaBootstrap
from spreadsheet.sheet.commands import CreateGroupSheet
from spreadsheet.wire.bootstrap import WireBootstrap
from spreadsheet.wire.commands import UpdateWire
from spreadsheet.wire.entity import Wire
from spreadsheet.wire.repository import WireRepo


def print_table(cells: list[Cell], size: tuple[int, int]):
    cells = deepcopy(cells)
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
    formula_repo = FormulaBootstrap().get_repo()
    cell_repo = CellBootstrap().get_repo()

    cmd = CreateGroupSheet(source_id=uuid4(), ccols=['sender', 'sub1'])
    cmd.execute()

    wire_repo: WireRepo = WireBootstrap().get_repo()
    old_wire = wire_repo.get_all()[0]

    cmd = UpdateWire(wire_id=old_wire.uuid, sender=-111)
    cmd.execute()

    cells = cell_repo.get_all()
    print_table(cells, (32, 2))


if __name__ == '__main__':
    print_hi()
