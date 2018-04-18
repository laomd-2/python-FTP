from socket import *
from utility.SocketHelper import SocketHelper


if __name__ == '__main__':
    client_socket = socket()
    client_socket.connect(("localhost", 12000))
    with open("a.txt", 'r') as file:
        for line in file:
            SocketHelper.send(client_socket, line)
    client_socket.close()
