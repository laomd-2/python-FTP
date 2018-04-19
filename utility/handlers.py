import socket
from .SocketHelper import SocketHelper
from socketserver import *
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
        self.client = socket.socket()

    def connect(self, address):
        self.client.connect(address)

    def disconnect(self):
        self.client.close()

    def send(self, some_object, coding='utf-8'):
        return SocketHelper.send(self.client, some_object, coding)

    def recv(self, buffersize, coding='utf-8'):
        return SocketHelper.recv(self.client, buffersize, coding)


class RequestHandler(BaseRequestHandler):
    def handle(self):
        pass

    def finish(self):
        pass

    def connect(self, address):
        self.request.connect(address)

    def disconnect(self):
        self.request.close()

    def send(self, some_object, coding='utf-8'):
        return SocketHelper.send(self.request, some_object, coding)

    def recv(self, buffersize, coding='utf-8'):
        return SocketHelper.recv(self.request, buffersize, coding)
