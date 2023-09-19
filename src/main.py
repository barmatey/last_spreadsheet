from spread.source.commands import CreateSourceNode
from messagebus.msgbus import SourceMsgbus
from spread.source.repository import SourceNodeRepo

msgbus = SourceMsgbus()
source_node_repo = SourceNodeRepo()


def foo():
    cmd = CreateSourceNode(msgbus=msgbus, repo=source_node_repo)
    execute(cmd)

    for key, value in msgbus.results.items():
        print(f"{key}:{value}")


def execute(cmd):
    msgbus.push_command(cmd)
    msgbus.run()


if __name__ == '__main__':
    # print_hi()
    foo()
