from utility.SocketHelper import SocketHelper
from socket import *


if __name__ == '__main__':
    all_client = []
    server_socket = socket()
    server_socket.bind(('', 13000))
    server_socket.listen(1)
    while True:
        client_socket, addr = server_socket.accept()
        msg = SocketHelper.recv(client_socket, 1024)
        print(msg, end=': ')
        if msg == "_register":
            print(addr)
            all_client.append(addr)
        elif msg == "_neighbors":
            print()
            SocketHelper.send(client_socket, all_client)
