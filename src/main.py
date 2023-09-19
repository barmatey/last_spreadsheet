import random
from uuid import UUID

from loguru import logger
#
# logger.remove(0)
# logger.add(sys.stderr, level="INFO")
from spread.formula.repository import FormulaNodeRepo
from spread.formula.collection.report_filter.commands import CreateReportFilters
from spread.formula.collection.plan_items.commands import CreatePlanItemsNode
from spread.source.commands import CreateSourceNode
from spread.wire.commands import CreateWireNode, UpdateWireNode


def create_wires(source_id: UUID) -> list[UUID]:
    commands = []
    for i in range(0, 4):
        commands.append(
            CreateWireNode(sender=i, receiver=i + 3, sub1="Hello", amount=random.random(), source_id=source_id)
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

    cmd = UpdateWireNode(uuid=wire_id, sender=1)
    cmd.execute()

    logger.success(f"plan_items_subs: {formula_repo.get_by_id(plan_items_id)._subs}")
    for sub in formula_repo.get_by_id(plan_items_id)._subs:
        logger.success(f"filter_by: {sub._value.filter_by}")


if __name__ == '__main__':
    # print_hi()
    foo()
