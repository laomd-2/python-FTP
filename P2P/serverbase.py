from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.client import ServerProxy
import urllib
import socket

# The use_builtin_types flag can be used to
# cause date/time values to be presented as datetime.datetime objects
# and binary data to be presented as bytes objects;
# this flag is false by default.
# datetime.datetime, bytes and bytearray objects
# may be passed to calls.


def getAddr():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


class BinaryServerProxy(ServerProxy):

    def __init__(self, url):
        super(BinaryServerProxy, self).__init__(url, use_builtin_types=True)


class ServerBase(SimpleXMLRPCServer):

    def __init__(self, url):
        self.url = url
        super(ServerBase, self).__init__(("", self.getPort(self.url)), logRequests=False)
        self.register_function(self.hello)
        self.register_function(self.query)

    def _start(self):
        print("starting up server",
              self.url, "...")
        self.onStart()
        print("server", self.url,
              "succeeded to start up. Ready to serve.")
        self.serve_forever()

    def onStart(self):
        pass

    def hello(self, other):
        print("say hello to", other)
        self.known.add(other)
        return 0

    def query(self, filename):
        pass

    @staticmethod
    def getPort(url):
        name = urllib.parse.urlparse(url)[1]
        patrs = name.split(':')
        return int(patrs[-1])
