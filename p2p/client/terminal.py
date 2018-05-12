from cmd import Cmd
from p2p.server.serverbase import BinaryServerProxy
from p2p.server.peer import Peer
from p2p.client.handleFault import Fault
from threading import Thread
from time import sleep
import sys


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
        try:
            self.peer.fetch(arg)
        except Fault as f:
            print("failed to fetch", arg, f)

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
