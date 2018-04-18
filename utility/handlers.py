import socket
from .SocketHelper import SocketHelper
import socketserver
from abc import ABCMeta, abstractmethod


class HandlerBase(object):
    __meta__ = ABCMeta

    def handle(self):
        pass

    def finish(self):
        pass

    @abstractmethod
    def connect(self, address):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def send(self, some_object):
        pass

    @abstractmethod
    def recv(self, buffersize):
        pass


class ResponseHandler(HandlerBase):

    def __init__(self):
        self.response = socket.socket()

    def connect(self, address):
        self.response.connect(address)

    def disconnect(self):
        self.response.close()

    def send(self, some_object, coding='utf-8'):
        return SocketHelper.send(self.response, some_object, coding)

    def recv(self, buffersize, coding='utf-8'):
        return SocketHelper.recv(self.response, buffersize, coding)


class RequestHandler(HandlerBase, socketserver.BaseRequestHandler):

    def connect(self, address):
        self.request.connect(address)

    def disconnect(self):
        self.request.close()

    def send(self, some_object, coding='utf-8'):
        return SocketHelper.send(self.request, some_object, coding)

    def recv(self, buffersize, coding='utf-8'):
        return SocketHelper.recv(self.request, buffersize, coding)


if __name__ == '__main__':
    client_socket = ResponseHandler()
    client_socket.connect(("localhost", 12000))
    with open("a.txt", 'r') as file:
        for line in file:
            SocketHelper.send(client_socket, line)
    client_socket.disconnect()
