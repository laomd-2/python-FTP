from serverbase import ServerBase, BinaryServerProxy
import sys


class Tracker(ServerBase):

    def __init__(self, url):
        super(Tracker, self).__init__(url)
        self.known = set()

    def query(self, filename, from_url):
        connected = []
        for url in self.known.copy():
            if url == from_url:
                continue
            print("quering", filename, "in", url, "...")
            try:
                s = BinaryServerProxy(url)
                if s.hasFile(filename):
                    print("founded in", url)
                    connected.append(url)
            except ConnectionRefusedError:
                print(url, "down, remove it from HMBP.")
                self.known.remove(url)
            except:
                pass
        return connected


def main():
    url = sys.argv[1]
    try:
        n = Tracker(url)
        n._start()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
