from socketserver import *
from utility.SocketHelper import SocketHelper


class MyServer(BaseRequestHandler):
    """docstring for MyServer"""

    def handle(self):
        with open("b.txt", 'w') as file:
            line = SocketHelper.recv(self.request, 1024)
            file.write(line)


if __name__ == '__main__':
    server = ThreadingTCPServer(('', 12000), MyServer)
    server.serve_forever()
