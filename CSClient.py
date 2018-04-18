from socket import *

if __name__ == '__main__':
    client_socket = socket()
    client_socket.connect(("172.18.32.225", 12000))
    with open("a.txt", 'rb') as file:
        for line in file:
            client_socket.send(line)
    client_socket.close()
