from socket import *
import os
from utility.SocketHelper import *
from utility.handlers import *
from socketserver import ThreadingTCPServer
from utility.transform import *


class HMBPServer(RequestHandler):
    """docstring for KMBPServer"""
    # def __init__(self):
    # port:端口号
    # super(HMBPServer,self).__init__()
    # self.serverPort = 12000
    # self.serverSocket = socket.socket()
    # self.serverSocket.bind(('',self.serverPort))
    # self.serverSocket.listen(10)
    # self.connectionSocket,self.addr = self.serverSocket.accept()

    def handle(self):
        while 1:
            message = self.recv(2048)
            if not message:
                break
            print('There is a client ask：' + message)
            if message == 'quit':
                self.shutDownConnect()
                self.finish()
                exit(1)
            elif message == 'dir':
                self.sendList()
            elif message == 'download':
                self.sendFile()
            elif message == 'upload':
                self.recvFile()

    def getClientSocket(self):
        """返回当前用户套接字"""
        pass

    def sendList(self):
        """列出文件目录，client_socket:客户套接字"""
        self.send('There are all files in the server:')
        lists = os.listdir('./server/')  # 获取当前路径下的所有文件
        self.send(lists)

    def sendFile(self):
        """发送文件给请求方"""
        filename = self.recv(1024)
        lists = os.listdir('./server/')

        if filename not in lists:
            self.send('0')
        else:
            self.send('1')
            TransformHelper.upload(self.request, './server/', filename)

    def recvFile(self):
        """接受文件"""
        TransformHelper.download(self.request, './server/')

    def shutDownConnect(self):
        self.disconnect()


if __name__ == '__main__':
    server = ThreadingTCPServer(('', 12000), HMBPServer)
    server.serve_forever()
