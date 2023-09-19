from dataclasses import dataclass

from spread.abstract.node import Event, Node


@dataclass
class TestSourceEvent(Event):
    node: Node
