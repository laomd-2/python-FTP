from xmlrpc.server import SimpleXMLRPCServer
from serverbase import ServerBase, BinaryServerProxy
from os.path import join, abspath, isfile
from handleFault import AccessDenied, UnhandledQuery
import sys
import time


SimpleXMLRPCServer.allow_reuse_address = 1


class Node(ServerBase):

    MAX_HISTORY_LENGTH = 6

    def __init__(self, url, tracker_url, dirname):
        super(Node, self).__init__(url)
        self.tracker_url = tracker_url
        self.dirname = dirname

    def onStart(self):
        self.tracker = BinaryServerProxy(self.tracker_url)
        self.tracker.hello(self.url)

    def query(self, filename):
        if self.hasFile(filename):
            ans = input(
                filename + " has been in local directory." +
                "Do you want to update it ?(y/n)")
            if ans == 'n':
                return None
        else:
            print("couldn't find", filename, "in local directory")
        return self._queryOther(filename)

    def fetch(self, filename):
        print("fetching", filename)
        result = self.query(filename)
        if result:
            f = open(join(self.dirname, filename), 'wb')
            f.write(result)
            f.close()
        print("done")
        return 0

    def hasFile(self, filename):
        file_dir = self.dirname
        filename = join(file_dir, filename)
        res = isfile(filename)
        return res

    def queryLocal(self, filename):
        print("search local", end="HMBP:~ ")
        return open(join(self.dirname, filename), 'rb').read()

    def _queryOther(self, filename):
        print("start to search others...")
        known = self.tracker.query(filename, self.url)
        for other in known:
            try:
                print("fetching from", other)
                s = BinaryServerProxy(other)
                return s.queryLocal(filename)
            except:
                pass
        raise UnhandledQuery


def main():
    url, tracker_url, directory = sys.argv[1:]
    try:
        n = Node(url, tracker_url, directory)
        n._start()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
