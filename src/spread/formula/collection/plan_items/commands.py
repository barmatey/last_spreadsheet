from uuid import UUID, uuid4

from loguru import logger
from pydantic import Field

import spread.formula
from spread.abstract.command import Command
from spread.abstract.pubsub import Pubsub, Publisher
from spread.source import usecase as source_usecase
from spread.wire.entity import Ccol
from . import usecase


class CreatePlanItemsNode(Command):
    source_id: UUID
    ccols: list[Ccol]
    uuid: UUID = Field(default_factory=uuid4)

    def execute(self) -> list[Publisher]:
        logger.info("CreatePlanItemsNode.execute()")

        # Create
        source_node = source_usecase.get_node_by_id(self.source_id)
        plan_items_node = usecase.create_node(self.ccols)
        source_node.subscribe([plan_items_node])

        # Save
        source_usecase.save_node(source_node)

        return [plan_items_node]
