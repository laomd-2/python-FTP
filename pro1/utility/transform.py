from utility.SocketHelper import *
import struct
import os


class TransformHelper(object):
    """docstring for transformHelper"""
    @staticmethod
    def download(src_socket, absolute_path='./'):
        """下载文件file_name到absolute_path，返回文件对象，没有该文件就抛异常"""
        # 交给服务器查找是否有该文件
        fileinfo_size = struct.calcsize('128sl')
        buf = SocketHelper.recv(src_socket, fileinfo_size, None)  # 接受数据包
        if buf:
            filename, filesize = struct.unpack('128sl', buf)  # 解压数据包，得到文件名字和大小
            newFileName = os.path.join(
                absolute_path, filename.decode().strip('\00'))
            recv_size = 0
            fp = open(newFileName, 'wb')  # 创建文件
            print('start receiving....' + str(filesize))
            ten_percent = int(filesize * 0.1)
            while not recv_size == filesize:  # 把文件内容读出来
                if filesize - recv_size > ten_percent:
                    data = SocketHelper.recv(src_socket, ten_percent, None)
                    # print (len(data))
                    recv_size += len(data)
                else:
                    data = SocketHelper.recv(
                        src_socket, filesize - recv_size, None)
                    # print (len(data))
                    recv_size = filesize
                fp.write(data)  # 把文件内容读进新创建的文件
                os.system('cls')
                print(str(recv_size) + '/' + str(filesize))
            fp.close()
            print('end receiving')

    @staticmethod
    def upload(src_socket, absolute_path='./', file_name=''):
        """上传文件，absolute_path：文件所在绝对路径，file_name:文件名字，返回是否上传成功"""

        filepath = absolute_path + file_name
        file_size = os.stat(filepath).st_size
        fhead = struct.pack('128sl', os.path.basename(
            filepath).encode(), file_size)
        ten_percent = int(file_size * 0.1)
        SocketHelper.send(src_socket, fhead)  # 发送文件头信息，包括名字和大小
        fp = open(filepath, 'rb')
        while 1:
            data = fp.read(ten_percent)
            # print(len(data))
            if not data:
                print('send over')
                break
            SocketHelper.send(src_socket, data)  # 发送文件内容
