from loguru import logger

from spreadsheet.abstract.event import Event
from spreadsheet.broker.handler import Handler


class WireUpdatedHandler(Handler):
    def handle(self):
        logger.error("WireUpdatedHandler")

    def parse_new_events(self) -> list[Event]:
        return []
