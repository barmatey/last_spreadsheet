from uuid import UUID, uuid4

from loguru import logger
from pydantic import Field

import spread.formula.collection.plan_items.usecase
import spread.formula.collection.report_filter.usecase
from spread.abstract.command import Command
from spread.abstract.pubsub import Pubsub


class CreateReportFilters(Command):
    plan_items_uuid: UUID
    uuid: UUID = Field(default_factory=uuid4)

    def execute(self) -> list[Pubsub]:
        logger.info("CreateReportFilters.execute()")
        plan_items_node = spread.formula.collection.plan_items.usecase.get_node_by_id(self.plan_items_uuid)
        report_filter_nodes = [spread.formula.collection.report_filter.usecase.create_node(i) for i in
                               range(0, len(plan_items_node.get_value().utable))]

        plan_items_node.subscribe(report_filter_nodes)
        spread.formula.collection.plan_items.usecase.save_node(plan_items_node)
        return report_filter_nodes


class DestroyReportFilter(Command):
    uuid: UUID

    def execute(self) -> list[Pubsub]:
        raise NotImplemented
