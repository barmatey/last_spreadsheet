from uuid import UUID, uuid4

from loguru import logger
from pydantic import Field

from spread.abstract.command import Command
from spread.formula.collection.plan_items import PlanItems, PlanItemsNode
from spread.formula.collection.report_filter import ReportFilter, ReportFilterNode
from spread.formula.repository import FormulaRepo
from spread.source.node import SourceNode
from spread.source.repository import SourceRepo
from spread.wire.model import Ccol


class CreatePlanItems(Command):
    source_id: UUID
    ccols: list[Ccol]
    uuid: UUID = Field(default_factory=uuid4)
    _result: UUID | None = None

    def execute(self):
        logger.info("CreatePlanItems.execute()")
        source_repo: SourceRepo = SourceRepo()
        source = source_repo.get_by_id(self.source_id)
        source_node = SourceNode(source)

        formula_repo: FormulaRepo = FormulaRepo()
        plan_items = PlanItems(ccols=self.ccols)
        formula_repo.add(plan_items)
        plan_items_node = PlanItemsNode(plan_items)

        source_node.subscribe([plan_items_node])

        self._result = plan_items.uuid

    def result(self):
        return self._result


class CreateReportFilters(Command):
    plan_items_uuid: UUID
    uuid: UUID = Field(default_factory=uuid4)
    _result: UUID | None = None

    def execute(self):
        logger.info("CreateReportFilters.execute()")
        formula_repo: FormulaRepo = FormulaRepo()
        plan_items: PlanItems = formula_repo.get_by_id(self.plan_items_uuid)

        report_filter_nodes = []
        for i in range(0, len(plan_items.utable)):
            report_filter = ReportFilter(index=i)
            formula_repo.add(report_filter)
            report_filter_nodes.append(ReportFilterNode(report_filter))

        PlanItemsNode(plan_items).subscribe(report_filter_nodes)

    def result(self):
        pass
