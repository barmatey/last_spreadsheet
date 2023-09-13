from copy import deepcopy
from uuid import uuid4

from loguru import logger

from spreadsheet.formula.bootstrap import FormulaBootstrap
from spreadsheet.sheet.commands import CreateGroupSheet
from spreadsheet.wire.bootstrap import WireBootstrap
from spreadsheet.wire.commands import UpdateWire
from spreadsheet.wire.repository import WireRepo


def print_hi():
    formula_repo = FormulaBootstrap().get_repo()

    cmd = CreateGroupSheet(source_id=uuid4(), ccols=['sender', 'sub1'])
    cmd.execute()

    wire_repo: WireRepo = WireBootstrap().get_repo()
    data = deepcopy(wire_repo.get_all()[0])
    data.sender = -111_000_000
    data = data.model_dump()
    data['wire_id'] = data.pop('uuid')

    cmd = UpdateWire(**data)
    cmd.execute()

    for row in formula_repo.get_all()[0].utable:
        logger.info(row)


if __name__ == '__main__':
    print_hi()
