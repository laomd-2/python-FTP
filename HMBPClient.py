import struct
import os
from utility.handlers import *


class HMBPClient(ResponseHandler):

    def __init__(self):
        super(HMBPClient, self).__init__()
        self.help_dic = {'help': 'get the help information',
                         'dir': 'list the orders',
                         'quit': 'quit the client',
                         'download': 'download file in the server'}

    def handle(self):
        while True:
            ask_inf = input('HMBPClient:> ').strip()
            if ask_inf == "quit":
                self.send(ask_inf)
                break
            else:
                func = getattr(self, ask_inf, None)
                if func is not None:
                    func()
                else:
                    print("Invalid command", ask_inf)

    def dir(self):
        """获取文件目录，
        返回文件名字符串列表"""
        self.send("dir")
        tips_mes = self.recv(1024)
        print(tips_mes)
        lists = self.recv(1024)
        for file_name in lists:
            print(file_name)

    def download(self):
        self.send("download")
        file_name = input('Please input the filename:')
        # absolute_path=input(
        # '\nabsolute path you want to save this file:'
        # )
        self._download('./', file_name)

    def upload(self):
        self.send("upload")
        file_name = input('Please input the file name:')
        self._upload('./', file_name)

    def help(self):
        for order, function in self.help_dic.items():
            print("%-10s" % order, function)

    def _download(self, absolute_path='./', file_name='recv_file'):
        """下载文件file_name到absolute_path，返回文件对象，没有该文件就抛异常"""
        # 交给服务器查找是否有该文件
        self.send(file_name)
        fileinfo_size = struct.calcsize('128sl')
        buf = self.recv(fileinfo_size, None)  # 接受数据包
        if buf:
            filename, filesize = struct.unpack('128sl', buf)  # 解压数据包，得到文件名字和大小
            newFileName = os.path.join(
                absolute_path, filename.decode().strip('\00'))
            recv_size = 0
            fp = open(newFileName, 'wb')  # 创建文件
            print('start receiving....' + str(filesize))
            ten_percent = int(filesize * 0.1)
            # number = 0
            while not recv_size == filesize:  # 把文件内容读出来
                if filesize - recv_size > ten_percent:
                    data = self.recv(ten_percent, None)
                    recv_size += len(data)
                else:
                    data = self.recv(filesize - recv_size, None)
                    recv_size = filesize
                fp.write(data)  # 把文件内容读进新创建的文件
                os.system('cls')
                print(str(recv_size) + '/' + str(filesize))
            fp.close()
            print('end receiving')

    def _upload(self, absolute_path, file_name):
        """上传文件，absolute_path：文件所在绝对路径，file_name:文件名字，返回是否上传成功"""

        filepath = absolute_path + file_name
        print(filepath)
        # os.stat() 方法用于在给定的路径上执行一个系统 stat 的调用,显示文件filepath信息
        file_size = os.stat(filepath).st_size
        fhead = struct.pack('128sl', os.path.basename(
            filepath).encode(), file_size)
        # struct.pack用于将Python的值根据格式符，转换为字符串（因为Python中没有字节(Byte)类型，可以把这里的字符串理解为字节流，或字节数组）
        ten_percent = int(file_size * 0.1)
        self.send(fhead)  # 发送文件头信息，包括名字和大小
        fp = open(filepath, 'rb')
        while 1:
            data = fp.read(ten_percent)
            if not data:
                print('send over')
                break
            self.send(data)  # 发送文件内容


if __name__ == '__main__':
    client = HMBPClient()
    client.connect(('localhost', 12000))
    client.handle()
    client.disconnect()
