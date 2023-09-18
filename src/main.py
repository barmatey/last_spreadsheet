import random

from uuid import UUID

from loguru import logger

from spreadsheet.broker.messagebus import MessageBus
from spreadsheet.source.commands import CreateSourceNode
from spreadsheet.wire.commands import CreateWireNode


def create_wires(source_id: UUID) -> list[UUID]:
    # commands = []
    # for i in range(0, 4):
    #     commands.append(
    #         CreateWireNode(sender=i, receiver=i + 3, sub1=f"MySubconto", amount=random.random(), source_id=source_id)
    #     )
    # results = []
    # for cmd in commands:
    #     cmd.execute()
    #     results.append(cmd.result())

    # return results
    pass


def foo():
    cmd = CreateSourceNode()
    execute(cmd)


def execute(cmd):
    bus = MessageBus()
    bus.push_command(cmd)
    bus.run()


if __name__ == '__main__':
    # print_hi()
    foo()
