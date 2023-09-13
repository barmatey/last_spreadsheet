from uuid import uuid4
from spreadsheet.sheet.commands import CreateGroupSheet


def print_hi():
    cmd = CreateGroupSheet(source_id=uuid4(), ccols=['sender', 'sub1'])
    cmd.execute()


if __name__ == '__main__':
    print_hi()

