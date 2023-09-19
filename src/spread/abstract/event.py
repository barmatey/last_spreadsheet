from spread.abstract.pubsub import Pubsub


class Event:
    def __init__(self, node: Pubsub):
        self.node = node
