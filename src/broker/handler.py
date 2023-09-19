from spread.abstract.event import Event
from spread.formula.collection.report_filter.events import ReportFilterDestroyed
from spread.formula.collection.report_filter import usecase as report_filter_usecase


def handle(event: Event):
    selector = {
        ReportFilterDestroyed: report_filter_usecase.destroy_node
    }
    selector[type(event)](event.node)

