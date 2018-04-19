import json


class SocketHelper(object):

    @staticmethod
    def send(src_socket, some_object, coding='utf-8'):
        """功能: some_object(不一定是bytes-like)转成bytes-like object，
                 并利用src_socket发送一个未转成bytes的对象
           返回值: 发送的字节数"""
        if not isinstance(some_object, bytes):
            try:
                some_object.decode()
            except AttributeError:
                some_object = json.dumps(some_object).encode()
        return src_socket.send(some_object)

    @staticmethod
    def recv(src_socket, buffersize, coding='utf-8'):
        """功能: 接收字节流(bytes-like object)并解码成正确的格式(字典、整数、字符串等)
           返回值: 解码后的对象"""
        data = src_socket.recv(buffersize)
        if coding is None:
            return data
        else:
            return json.loads(data.decode())
