from socket import *
from utility.transform import *
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
connectionSocket, addr = serverSocket.accept()
# 调用accept方法时，socket会时入“waiting”状态。客户请求连接时，方法建立连接并返回服务器。
# accept方法返回一个含有两个元素的元组(connection,address)。
# 第一个元素connection是新的socket对象，服务器必须通过它与客户通信；
# 第二个元素 address是客户的Internet地址。

while True:
    message = SocketHelper.recv(connectionSocket, 2048)
    if not message:
        break
    print('There is a client ask：' + addr[0] + ',' + message)
    if message == 'quit':
        connectionSocket.close()
        serverSocket.close()
        break
    elif message == 'dir':
        SocketHelper.send(connectionSocket,
                          'There are all files in the server:')
        lists = os.listdir('./server/')  # 获取当前路径下的所有文件
        SocketHelper.send(connectionSocket, lists)
    elif message == 'download':
        filename = SocketHelper.recv(connectionSocket, 1024)
        TransformHelper.upload(connectionSocket, './server/', filename)

    elif message == 'upload':
        TransformHelper.download(connectionSocket, './server/')


# 服务器和客户端通过send和recv方法通信(传输 数据)。
# 服务器调用send，并采用字符串形式向客户发送信息。send方法返回已发送的字符个数。
# 服务器使用recv方法从客户接收信息。调用recv 时，服务器必须指定一个整数，它对应于可通过本次方法调用来接收的最大数据量。
# recv方法在接收数据时会进入“blocked”状态，最后返回一个字符串，用它表示收到的数据。
# 如果发送的数据量超过了recv所允许的，数据会被截短。多余的数据将缓冲于接收端。以后调用recv时，
# 多余的数据会从缓冲区 删除(以及自上次调用recv以来，客户可能发送的其它任何数据)。
