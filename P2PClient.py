from ..csserver.CSClient import CSClient


class P2PClient(CSClient):
    """client for p2p"""

    def __init__(self):
        """create and register a TCP client"""
        super(P2PClient, self).__init__()
        pass

    @property
    def neighbors(self):
        """return an iterable object of client socket"""
        pass

    @property
    def files(self):
        """return an iterable object of filename in current pc"""
        pass


if __name__ == '__main__':
    pass
