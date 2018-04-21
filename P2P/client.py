from cmd import Cmd
from random import choice
from string import ascii_lowercase
from server import Node, BinaryServerProxy
from threading import Thread
from time import sleep
import sys

HEAD_START = 0.1  # Seconds
SECRET_LENFGTH = 100


def randomString(length):
    chars = []
    letters = ascii_lowercase[:26]
    while length > 0:
        length -= 1
        chars.append(choice(letters))
    return ''.join(chars)


class Client(Cmd):
    prompt = 'HMBP:~ '

    def __init__(self, url, dirname, urlfile):
        print("Welcome to HMBP!")
        Cmd.__init__(self)
        self.secret = randomString(SECRET_LENFGTH)
        n = Node(url, dirname, self.secret)
        t = Thread(target=n._start)
        t.setDaemon(1)
        t.start()
        sleep(HEAD_START)
        # The use_builtin_types flag can be used to
        # cause date/time values to be presented as datetime.datetime objects
        # and binary data to be presented as bytes objects;
        # this flag is false by default.
        # datetime.datetime, bytes and bytearray objects
        # may be passed to calls.
        self.server = BinaryServerProxy(url)
        for line in open(urlfile):
            line = line.strip()
            self.server.hello(line)

    def do_fetch(self, arg):
        self.server.fetch(arg, self.secret)

    def do_exit(self, arg):
        print("Goodbye!")
        sys.exit()

    do_EOF = do_exit


def main():
    urlfile, directory, url = sys.argv[1:]
    try:
        client = Client(url, directory, urlfile)
        client.cmdloop()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
