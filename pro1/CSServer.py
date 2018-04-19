from socketserver import ThreadingTCPServer
from utility.handlers import RequestHandler


class CSServer(RequestHandler):

    def handle(self):
        with open("b.txt", 'w') as file:
            line = self.recv(1024)
            file.write(line)


if __name__ == '__main__':
    server = ThreadingTCPServer(('', 12000), CSServer)
    server.serve_forever()
