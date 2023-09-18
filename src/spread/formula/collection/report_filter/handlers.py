from loguru import logger

from spread.formula.collection.plan_items.entity import PlanItemsNode


def handle_plan_items_node_updated(node: PlanItemsNode):
    logger.debug("handle_plan_items_node_updated")
