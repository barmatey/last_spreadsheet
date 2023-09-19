from uuid import UUID

from spread.abstract.pubsub import Subscriber
from spread.formula.collection.plan_items.entity import PlanItemsNode, PlanItems
from spread.formula.repository import FormulaNodeRepo
from spread.wire.entity import Ccol


def create_node(ccols: list[Ccol]) -> PlanItemsNode:
    entity = PlanItems(ccols=ccols)
    node = PlanItemsNode(entity)
    FormulaNodeRepo().add(node)
    return node


def get_node_by_id(uuid: UUID) -> PlanItemsNode:
    node = FormulaNodeRepo().get_by_id(uuid)
    if not isinstance(node, PlanItemsNode):
        raise TypeError
    return node


def save_node(data: PlanItemsNode):
    FormulaNodeRepo().update(data)
