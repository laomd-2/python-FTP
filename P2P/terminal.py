from cmd import Cmd
from serverbase import BinaryServerProxy
from peer import Peer
from threading import Thread
from time import sleep
import sys
from handleFault import Fault


HEAD_START = 0.1  # Seconds


class Terminal(Cmd):
    prompt = 'HMBP:~ '

    def __init__(self, dirname):
        print("Welcome to HMBP!")
        Cmd.__init__(self)
        n = Peer(dirname)
        t = Thread(target=n._start)
        t.setDaemon(1)
        t.start()
        sleep(HEAD_START)
        self.peer = BinaryServerProxy(n.url)

    def do_fetch(self, arg):
        # try:
            self.peer.fetch(arg)
        # except Fault:
        #     print("failed to fetch", arg)

    def do_exit(self, arg):
        print("Goodbye!")
        sys.exit()

    do_EOF = do_exit


def main():
    directory = sys.argv[1]
    try:
        client = Terminal(directory)
        client.cmdloop()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
