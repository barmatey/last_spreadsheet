from spread.abstract.node import MessageBus
from spread.source.commands import CreateSourceNode
from spread.source.repository import SourceNodeRepo

msgbus = MessageBus()
source_node_repo = SourceNodeRepo()


def foo():
    cmd = CreateSourceNode(msgbus=msgbus, repo=source_node_repo)
    execute(cmd)

    for key, value in msgbus.results.items():
        print(f"{key}:{value}")


def execute(cmd):
    bus = MessageBus()
    bus.push_command(cmd)
    bus.run()


if __name__ == '__main__':
    # print_hi()
    foo()
