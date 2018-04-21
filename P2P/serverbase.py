from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.client import ServerProxy
import urllib
from random import choice
from string import ascii_lowercase


# The use_builtin_types flag can be used to
# cause date/time values to be presented as datetime.datetime objects
# and binary data to be presented as bytes objects;
# this flag is false by default.
# datetime.datetime, bytes and bytearray objects
# may be passed to calls.


class BinaryServerProxy(ServerProxy):

    def __init__(self, url):
        super(BinaryServerProxy, self).__init__(url, use_builtin_types=True)


class ServerBase(object):
    SECRET_LENFGTH = 100

    def __init__(self, url):
        self.url = url

    def _start(self):
        print("starting up server",
              self.url, "...")
        s = SimpleXMLRPCServer(("", self.getPort(self.url)), logRequests=False)
        s.register_instance(self)
        self.onStart()
        print("server", self.url,
              "succeeded to start up. Ready to serve.")
        s.serve_forever()

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
