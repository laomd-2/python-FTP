from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.client import ServerProxy, Fault
from os.path import join, abspath, isfile
import sys
import urllib


SimpleXMLRPCServer.allow_reuse_address = 1
MAX_HISTORY_LENGTH = 6

UNHANDLED = 100
ACCESS_ENIED = 200


class UnhandledQuery(Fault):

    def __init__(self, message="Couldn't handle the query"):
        Fault.__init__(self, UNHANDLED, message)


class AccessDenied(Fault):

    def __init__(self, message="Access denied"):
        Fault.__init__(self, ACCESS_ENIED, message)


def inside(dir, name):
    dir = abspath(dir)
    name = abspath(name)
    return name.startswith(join(dir, ''))


def getPort(url):
    name = urllib.parse.urlparse(url)[1]
    patrs = name.split(':')
    return int(patrs[-1])


class Node:

    def __init__(self, url, dirname, secret):
        self.url = url
        self.dirname = dirname
        self.secret = secret
        self.known = set()

    def query(self, query, history=[]):
        try:
            print("search local", end="\nHMBP:~ ")
            return self._handle(query)
        except UnhandledQuery:
            history = history + [self.url]
            if len(history) >= MAX_HISTORY_LENGTH:
                raise
            print("file", query, "not exist local, start to search others")
            return self._broadcast(query, history)

    def hello(self, other):
        print("say hello to", other)
        self.known.add(other)
        return 0

    def fetch(self, query, secret):
        print("server.fetch")
        if secret != self.secret:
            raise AccessDenied
        print("fetching", query)
        result = self.query(query)
        print("succeeded" if result else "failed", "to fetch", query)
        f = open(join(self.dirname, query), 'w')
        f.write(result)
        f.close()
        return 0

    def _start(self):
        print("starting up server", self.url, "...")
        s = SimpleXMLRPCServer(("", getPort(self.url)), logRequests=False)
        s.register_instance(self)
        print("server", self.url, "succeeded to start up. Ready to serve.")
        s.serve_forever()

    def _handle(self, query):
        dir = self.dirname
        name = join(dir, query)
        if not isfile(name):
            raise UnhandledQuery
        if not inside(dir, name):
            raise AccessDenied
        return open(name).read()

    def _broadcast(self, query, history):
        for other in self.known.copy():
            if other in history:
                continue
            try:
                print("search", other)
                s = ServerProxy(other)
                print("start to query", other)
                return s.query(query, history)
            except Fault:
                self.known.remove(other)
                # if Fault.faultCode == UNHANDLED: pass
                # else: self.known.remove(other)
            except:
                self.known.remove(other)
        raise UnhandledQuery


def main():
    url, directory, secret = sys.argv[1:]
    n = Node(url, directory, secret)
    n._start()


if __name__ == '__main__':
    main()
