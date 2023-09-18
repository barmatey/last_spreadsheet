from spread.formula.collection.report_filter.entity import ReportFilterNode, ReportFilter
from spread.formula.repository import FormulaNodeRepo


def create_node(index: int) -> ReportFilterNode:
    entity = ReportFilter(index=index)
    node = ReportFilterNode(entity)
    FormulaNodeRepo().add(node)
    return node


def save_node(data: ReportFilterNode):
    FormulaNodeRepo().update(data)
