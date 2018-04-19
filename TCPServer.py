from socket import *
import os
import struct  # struct模块
from utility.SocketHelper import *
serverPort = 12000
# 建立socker套接字，两个参数，family代表家族地址，可为AF_INET或AF_UNIX。AF_INET家族包括Internet地址，AF_UNIX家族用于同一台机器上的进程间通信。
# type代表套接字类型，可为SOCK_STREAM(流套接字)和SOCK_DGRAM(数据报套接字)，type默认TCP
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))  # 将端口号12000与某个服务器套接字绑定，socket绑定到指定地址。
# 由AF_INET所创建的套接字，address地址必须是一个双元素元组，格式是(host,port)。host代表主机，port代表端口号。
# 如果端口号正在使用、主机名不正确或端口已被保留，bind方法将引发socket.error异常
serverSocket.listen(10)  # 请求连接的最大数量,同时挂起的最大数量
# 指定最多允许多少个客户连接到服务器。它的值至少为1。收到连接请求后，这些请求需要排队，如果队列满，就拒绝请求。
print('The server is ready to receive')
# 创建新套接字connectionSocket为用户专用，服务器套接字通过socket的accept方法等待客户请求一个连接

# 调用accept方法时，socket会时入“waiting”状态。客户请求连接时，方法建立连接并返回服务器。
# accept方法返回一个含有两个元素的元组(connection,address)。
# 第一个元素connection是新的socket对象，服务器必须通过它与客户通信；
# 第二个元素 address是客户的Internet地址。
connectionSocket, addr = serverSocket.accept()
while True:
    message = SocketHelper.recv(connectionSocket, 2048)
    if message:
        print('There is a client ask：' + addr[0] + ',' + message)
        if message == 'dir':
            SocketHelper.send(connectionSocket,
                              'There are all files in the server:')
            lists = os.listdir('E:/new/')  # 获取当前路径下的所有文件
            SocketHelper.send(connectionSocket, lists)
        elif message == 'download':
            filename = SocketHelper.recv(connectionSocket, 1024)
            filepath = 'E:/new/' + filename
            print(filepath)
            # os.stat() 方法用于在给定的路径上执行一个系统 stat 的调用,显示文件filepath信息
            file_size = os.stat(filepath).st_size
            fhead = struct.pack('128sl', os.path.basename(
                filepath).encode(), file_size)
            # struct.pack用于将Python的值根据格式符，转换为字符串（因为Python中没有字节(Byte)类型，可以把这里的字符串理解为字节流，或字节数组）
            ten_percent = int(file_size * 0.1)
            SocketHelper.send(connectionSocket, fhead)
            # connectionSocket.send(fhead)      #发送文件头信息，包括名字和大小
            fp = open(filepath, 'rb')
            while 1:
                data = fp.read(ten_percent)
                if not data:
                    print('send over')
                    break
                SocketHelper.send(connectionSocket, data)
                # connectionSocket.send(data)     #发送文件内容
        elif message == 'upload':

            fileinfo_size = struct.calcsize('128sl')
            buf = SocketHelper.recv(connectionSocket, fileinfo_size, None)
            # buf=connectionSocket.recv(fileinfo_size)              #接受数据包
            if buf:
                filename, filesize = struct.unpack(
                    '128sl', buf)  # 解压数据包，得到文件名字和大小
                newFileName = os.path.join(
                    'E:/new/', filename.decode().strip('\00'))
                recv_size = 0
                fp = open(newFileName, 'wb')  # 创建文件
                print('start receiving....' + str(filesize))
                ten_percent = int(filesize * 0.1)
                number = 0
                while not recv_size == filesize:  # 把文件内容读出来
                    if filesize - recv_size > ten_percent:

                        data = SocketHelper.recv(
                            connectionSocket, ten_percent, None)
                        recv_size += len(data)
                    else:
                        data = SocketHelper.recv(
                            connectionSocket, filesize - recv_size, None)
                        recv_size = filesize
                    fp.write(data)  # 把文件内容读进新创建的文件
                    os.system('cls')
                    print(str(recv_size) + '/' + str(filesize))
                fp.close()
                print('end receiving')
serverSocket.close()
# 服务器和客户端通过send和recv方法通信(传输 数据)。
# 服务器调用send，并采用字符串形式向客户发送信息。send方法返回已发送的字符个数。
# 服务器使用recv方法从客户接收信息。调用recv 时，服务器必须指定一个整数，它对应于可通过本次方法调用来接收的最大数据量。
# recv方法在接收数据时会进入“blocked”状态，最后返回一个字符串，用它表示收到的数据。
# 如果发送的数据量超过了recv所允许的，数据会被截短。多余的数据将缓冲于接收端。以后调用recv时，
# 多余的数据会从缓冲区 删除(以及自上次调用recv以来，客户可能发送的其它任何数据)。
