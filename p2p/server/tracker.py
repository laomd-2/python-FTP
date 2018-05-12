from p2p.server.serverbase import ServerBase, BinaryServerProxy


TRACKER_URL = "http://172.18.35.248:12000"


class Tracker(ServerBase):

    def __init__(self, url):
        super(Tracker, self).__init__(url)
        self.known = set()

    def query(self, filename, from_url):
        connected = []
        length = 0
        for url in self.known.copy():
            if url == from_url:
                continue
            print("quering", filename, "in", url, "...")
            try:
                s = BinaryServerProxy(url)
                if s.hasFile(filename):
                    length = s.bytesLength(filename)
                    print("founded in", url)
                    connected.append(url)
            except ConnectionRefusedError:
                print(url, "down, remove it from HMBP.")
                self.known.remove(url)
            except:
                pass
        return length, connected


def main():
    try:
        n = Tracker(TRACKER_URL)
        n._start()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
