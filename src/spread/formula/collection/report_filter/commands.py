from uuid import UUID, uuid4

from loguru import logger
from pydantic import Field

import spread.formula.collection.plan_items.usecase
import spread.formula.collection.report_filter.usecase
from spread.abstract.command import Command


class CreateReportFilters(Command):
    plan_items_uuid: UUID
    uuid: UUID = Field(default_factory=uuid4)
    _result: UUID | None = None

    def execute(self):
        logger.info("CreateReportFilters.execute()")
        plan_items_node = spread.formula.collection.plan_items.usecase.get_node_by_id(self.plan_items_uuid)
        report_filter_nodes = [spread.formula.collection.report_filter.usecase.create_node(i) for i in
                               range(0, len(plan_items_node.get_value().utable))]

        plan_items_node.subscribe(report_filter_nodes)

        spread.formula.collection.plan_items.usecase.save_node(plan_items_node)
        for node in report_filter_nodes:
            spread.formula.collection.report_filter.usecase.save_node(node)

    def result(self):
        pass


class DestroyReportFilter(Command):
    uuid: UUID

    def execute(self):
        logger.info("DestroyReportFilter.execute()")

    def result(self):
        pass
