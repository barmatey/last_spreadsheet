from abc import ABC
from uuid import UUID

from spread.abstract.pubsub import Pubsub


class FormulaNode(Pubsub, ABC):
    uuid: UUID
