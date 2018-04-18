from socketserver import *


class MyServer(BaseRequestHandler):
    """docstring for MyServer"""

    def handle(self):
        with open("a.txt", 'wb') as file:
            line = self.request.recv(1024)
            file.write(line)


if __name__ == '__main__':
    server = ThreadingTCPServer(('', 12000), MyServer)
    server.serve_forever()
