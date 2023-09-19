from spread.abstract.event import Event
from spread.formula.collection.report_filter.events import ReportFilterDestroyed


def handle(event: Event):
    selector = {
        ReportFilterDestroyed: lambda x: print(x)
    }
    selector[type(event)](event.node)

