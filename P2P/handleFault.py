from xmlrpc.client import Fault

UNHANDLED = 100


class UnhandledQuery(Fault):

    def __init__(self, message="Couldn't handle the query"):
        Fault.__init__(self, UNHANDLED, message)
