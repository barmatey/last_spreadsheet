from uuid import uuid4

from loguru import logger

from spreadsheet.formula.bootstrap import FormulaBootstrap
from spreadsheet.sheet.commands import CreateGroupSheet
from spreadsheet.wire.bootstrap import WireBootstrap
from spreadsheet.wire.commands import UpdateWire
from spreadsheet.wire.entity import Wire
from spreadsheet.wire.repository import WireRepo


def print_hi():
    formula_repo = FormulaBootstrap().get_repo()

    cmd = CreateGroupSheet(source_id=uuid4(), ccols=['sender', 'sub1'])
    cmd.execute()

    wire_repo: WireRepo = WireBootstrap().get_repo()
    old_wire = wire_repo.get_all()[0]

    cmd = UpdateWire(wire_id=old_wire.uuid, sender=-111_111_111)
    cmd.execute()


if __name__ == '__main__':
    print_hi()
