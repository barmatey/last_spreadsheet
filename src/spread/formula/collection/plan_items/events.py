from spread.abstract.pydantic_model import PydanticModel
from spread.formula.collection.report_filter.entity import ReportFilterNode
from spread.formula.collection.report_filter import usecase as report_filter_usecase
from .entity import PlanItemsNode
from . import usecase as plan_items_usecase


class PlanItemsUpdated(PydanticModel):
    node: PlanItemsNode

    def handle(self):
        old_len = len(self.node.get_old_value().utable)
        new_len = len(self.node.get_old_value().utable)
        if new_len < old_len:
            # Find subs to drop
            subs_to_detach = []
            for sub in self.node.get_subs():
                if isinstance(sub, ReportFilterNode):
                    if sub.get_value().index >= new_len:
                        subs_to_detach.append(sub)

            # Unsubscribe
            self.node.unsubscribe(subs_to_detach)

            # Save
            plan_items_usecase.save_node(self.node)
            for sub in self.node.get_subs():
                pass
