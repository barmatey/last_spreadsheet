from uuid import UUID, uuid4

from loguru import logger
from pydantic import Field

from spread.abstract.command import Command
from spread.formula.collection.plan_items import PlanItems, PlanItemsNode
from spread.formula.collection.report_filter import ReportFilter, ReportFilterNode
from spread.formula.repository import FormulaNodeRepo
from spread.source.node import SourceNode
from spread.source.repository import SourceRepo
from spread.wire.entity import Ccol

from spread.source import usecase as source_usecase
from spread.formula.collection import plan_items
from spread.formula.collection import report_filter


class CreatePlanItemsNode(Command):
    source_id: UUID
    ccols: list[Ccol]
    uuid: UUID = Field(default_factory=uuid4)
    _result: UUID | None = None

    def execute(self):
        logger.info("CreatePlanItemsNode.execute()")

        # Create
        source_node = source_usecase.get_node_by_id(self.source_id)
        plan_items_node = plan_items.create_node(self.ccols)
        source_node.subscribe([plan_items_node])

        # Save
        source_usecase.save_node(source_node)
        plan_items.save_node(plan_items_node)

        # Result
        self._result = plan_items_node.uuid

    def result(self):
        return self._result


class CreateReportFilters(Command):
    plan_items_uuid: UUID
    uuid: UUID = Field(default_factory=uuid4)
    _result: UUID | None = None

    def execute(self):
        logger.info("CreateReportFilters.execute()")
        plan_items_node = plan_items.get_node_by_id(self.plan_items_uuid)
        report_filter_nodes = [report_filter.create_node(i) for i in range(0, len(plan_items_node.get_value().utable))]

        plan_items_node.subscribe(report_filter_nodes)

        plan_items.save_node(plan_items_node)
        for node in report_filter_nodes:
            report_filter.save_node(node)

    def result(self):
        pass
