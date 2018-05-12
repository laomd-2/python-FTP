from xmlrpc.server import SimpleXMLRPCServer
from serverbase import ServerBase, BinaryServerProxy, getAddr
from os.path import join
from handleFault import UnhandledQuery
from tracker import TRACKER_URL
import sys
from random import randint


SimpleXMLRPCServer.allow_reuse_address = 1


class Peer(ServerBase):

    MAX_HISTORY_LENGTH = 6

    def __init__(self, dirname):
        myaddr = getAddr()
        self.url = "http://" + myaddr + ":" + str(randint(12000, 13000))
        super(Peer, self).__init__(self.url)
        self.register_function(self.fetch)
        self.register_function(self.send)
        self.register_function(self.hasFile)
        self.register_function(self.bytesLength)
        self.dirname = dirname

    def onStart(self):
        self.tracker = BinaryServerProxy(TRACKER_URL)
        self.tracker.hello(self.url)

    def query(self, filename):
        if self.hasFile(filename):
            ans = input(
                filename + " has been in local directory." +
                "Do you want to update it ?(y/n)")
            if ans == 'n':
                return None
        return self._fetchFromOthers(filename)

    def fetch(self, filename):
        print("fetching", filename)
        result = self.query(filename)
        if result:
            f = open(join(self.dirname, filename), 'wb')
            for block in result:
                f.write(block)
            f.close()
            print("done")
        return 0

    def hasFile(self, filename):
        return not self.bytesLength(filename) == 0

    def bytesLength(self, filename):
        file_dir = self.dirname
        filename = join(file_dir, filename)
        try:
            with open(filename, 'rb') as f:
                return len(f.read())
        except FileNotFoundError:
            return 0

    def send(self, filename, start, length):
        print("sending", filename, '[', start, ',',
              start + length, ')', end="\nHMBP:~ ")
        return open(join(self.dirname, filename), 'rb') \
            .read()[start: start + length]

    def _fetchFromOthers(self, filename):
        print("start to search others...")
        total_length, known = self.tracker.query(filename, self.url)
        num = len(known)
        if num == 0:
            raise UnhandledQuery
        else:
            length = total_length // num
            begin = 0
            if not total_length % num == 0:
                length += 1
            total = []
            for other in known:
                s = BinaryServerProxy(other)
                a = s.send(filename, begin, length)
                total.append(a)
                tmp_len = begin + length
                if tmp_len > total_length:
                    tmp_len = total_length
                print("fetched", other, "[", begin, ',', tmp_len, ')')
                begin = tmp_len
            print("fetch from", num, "peers")
            return total


def main():
    directory = sys.argv[1]
    try:
        n = Peer(directory)
        n._start()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
