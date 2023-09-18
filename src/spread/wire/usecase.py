from datetime import datetime
from uuid import UUID, uuid4

from spread.wire.entity import Wire
from spread.wire.node import WireNode
from spread.wire.repository import WireNodeRepo


def create_node(currency: str, sender: float, receiver: float, amount: float, date: datetime = None,
                sub1: str = "", sub2: str = "", comment: str = "", uuid: UUID = None) -> WireNode:
    if date is None:
        date = datetime.now()
    if uuid is None:
        uuid = uuid4()

    wire = Wire(currency=currency, sender=sender, receiver=receiver, amount=amount, date=date,
                sub1=sub1, sub2=sub2, comment=comment, uuid=uuid)
    node = WireNode(wire)
    repo = WireNodeRepo()
    repo.add(node)
    return node


def get_node_by_id(uuid: UUID) -> WireNode:
    repo = WireNodeRepo()
    node = repo.get_by_id(uuid)
    return node


def update_node_value(uuid: UUID, data: dict):
    repo = WireNodeRepo()
    node = repo.get_by_id(uuid)
    node.set_entity_fields(data)


def save_node(data: WireNode):
    repo = WireNodeRepo()
    repo.update(data)
