from spread.abstract.pubsub import Subscriber
from spread.abstract.pydantic_model import PydanticModel
from spread.formula.collection.plan_items.entity import PlanItems
from spread.formula.collection.report_filter.entity import ReportFilter


class PlanItemsUpdated(PydanticModel):
    old_value: PlanItems
    new_value: PlanItems
    subs: list[Subscriber]

    def handle(self):
        old_len = len(self.old_value.utable)
        new_len = len(self.new_value.utable)
        if new_len < old_len:
            for sub in self.subs:
                if isinstance(sub, ReportFilter):
                    if sub.index >= new_len:
                        pass
