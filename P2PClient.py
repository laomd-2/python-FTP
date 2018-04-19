from HMBPClient import HMBPClient
from socket import socket


class P2PClient(HMBPClient):
    """docstring for P2PClient"""

    def __init__(self):
        super(P2PClient, self).__init__()
        self.to_tracker = socket()
        self.register()

    @property
    def neighbors(self):
        self.__save()
        self.client = self.to_tracker
        self.send("_neighbors")
        res = self.recv(1024)
        self.__reset()
        return res

    def download(self, absolute_path='./', file_name='recv_file'):
        self.send(file_name)
        print(self.neighbors)
        # to_neighbor = socket()
        # self.__save()
        # self.client = to_neighbor
        # for neighbor in self.neighbors:
        #     self.connect((neighbor, 14000))
        #     files = self.dir()
        #     if file_name in files:
        #         print("download from", neighbor)
        #         break
        #     self.disconnect()
        # else:  # 客户端没有, 向服务器请求文件
        #     print("download from server.")
        #     self.__reset()
        # super(HMBPClient, self).download(absolute_path, file_name)
        # self.__reset()

    def __save(self):
        self.tmp_client = self.client

    def __reset(self):
        self.client = self.tmp_client

    def register(self):
        self.__save()
        self.client = self.to_tracker
        self.connect(('localhost', 13000))
        self.send("_register")
        self.__reset()


if __name__ == '__main__':
    client = P2PClient()
    client.connect(('localhost', 12000))
    client.handle()
    client.disconnect()
