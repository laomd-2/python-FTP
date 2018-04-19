#!/usr/bin/env python
# -*- coding=utf-8 -×-

from xmlrpclib import ServerProxy
from os.path import join, isfile
from SimpleXMLRPCServer import SimpleXMLRPCServer
from urlparse import urlparse
import sys

MAX_HISTORY_LENGTH = 6

OK = 1
FAIL = 2
EMPTY = ''

def getPort(url):
    """
    根据url获取端口号
    """
    name = urlparse(url)[1]
    parts = name.split(":")
    return int(parts[-1])

class Node:
    """
    P2P网络中的节点
    """
    def __init__(self, url, directory, secret):
        self.url = url
        self.directory = directory
        self.secret = secret
        self.know = set()

    def query(self, query, history=[]):
        """
        查找文件，先在本机查找，如果找到则返回，找不到则查找其他已知节点
        """
        code, data = self._handle(query)
        if code == OK:
            return code, data
        else:
            # 添加到history，标记查找的深度
            history = history + [self.url]
            if len(history) >= MAX_HISTORY_LENGTH:
                return FAIL, EMPTY
            return self._broadcast(query, history)

    def hello(self, other):
        """
        认识其他节点，将其他节点的地址添加到本服务器的列表
        """
        self.know.add(other)
        return OK
    def fetch(self, query, secret):
        """
        用于从节点下载数据
        """
        if secret != self.secret:
            return FAIL
        code, data = self.query(query)
        if code == OK:
            # 把查询到的数据写到本地
            f = open(join(self.directory, query), 'w')
            f.write(data)
            f.close()
            return OK
        return FAIL

    def _start(self):
        """
        内部使用，用于启动XML_RPC服务器
        """
        server = SimpleXMLRPCServer(("", getPort(self.url)), logRequests=False)
        server.register_instance(self)
        server.serve_forever()

    def _handle(self, query):
        """
        搜索文件在本服务器上是否存在
        """
        dirs = self.directory
        name = join(dirs, query)
        if not isfile(name):
            return FAIL, EMPTY
        return OK, open(name).read()

    def _broadcast(self, query, history):
        """
        内部时使用，用于将查询广播到其他已知节点
        """
        for other in self.know.copy():
            try:
                # 根据url创建远程节点的proxy，使用xml_rpc进行远程调用
                server = ServerProxy(other)
                code, data = server.query(query, history)
                if code == OK:
                    return code, data
            except:
                # 说明该server已经不可用
                self.know.remove(other)
        # 如果在所有节点中没有找到，就返回空
        return FAIL, EMPTY



def main():
    url, directory, secret = sys.argv[1:]
    node = Node(url, directory, secret)
    node._start()

if __name__ == '__main__':
    main()

