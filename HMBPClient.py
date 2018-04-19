from utility.transform import *
import os
from utility.handlers import *


class HMBPClient(ResponseHandler):
    """docstring for Peer"""

    def __init__(self):
        super(HMBPClient, self).__init__()
        self.help_dic = {
            'help': 'get the help information',
            'dir': 'list the files',
            'quit': 'quit the client',
            'download': 'download file from the server to your client',
            'upload': 'upload file from your client to server'}

    def handle(self):
        while 1:
            print('\nHMBPServer:>', end='')
            ask_inf = input().strip()
            if ask_inf == 'help':
                self.showHelp()
            elif ask_inf == 'quit':
                self.send(ask_inf)
                return
            elif ask_inf == 'dir':
                choice = input('1.client\t2.server\n')
                if choice == '2':
                    self.send(ask_inf)
                lists = self.dir(choice)
                for file_name in lists:
                    print(file_name)

            elif ask_inf == 'download':
                self.send(ask_inf)
                file_name = input('Please input the filename:')
                self.download('./client/', file_name)
            elif ask_inf == 'upload':
                file_name = input(
                    'Please input the file name you want to upload:')
                self.upload('./client/', file_name, ask_inf)

    def dir(self, choice):
        """获取文件目录，
        返回文件名字符串列表"""
        if choice == '2':
            tips_mes = self.recv(1024)
            print(tips_mes)
            lists = self.recv(1024)
        else:
            print("There are the files in the client")
            lists = os.listdir('./client/')
        return lists

    def download(self, absolute_path='./client/', file_name=''):
        """下载文件file_name到absolute_path，返回文件对象，没有该文件就抛异常"""
        # 交给服务器查找是否有该文件
        self.send(file_name)
        mes = self.recv(1024)
        if mes == '0':
            print("The file does not exist.")
        else:
            TransformHelper.download(self.response, absolute_path)

    def upload(self, absolute_path='./client/', file_name='', ask_inf=''):
        """上传文件，absolute_path：文件所在绝对路径，file_name:文件名字，返回是否上传成功"""
        lists = os.listdir('./client/')
        if file_name not in lists:
            print('The file does not exist.')
        else:
            self.send(ask_inf)
            TransformHelper.upload(self.response, absolute_path, file_name)

    def showHelp(self):
        for order, function in self.help_dic.items():
            print("%-10s" % order, function)  # ...


if __name__ == '__main__':
    client = HMBPClient()
    client.connect(('localhost', 12000))
    # client.connect(('192.168.155.2', 12000))
    client.handle()
    client.disconnect()
