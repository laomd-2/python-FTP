#!/usr/bin/env python
# -*- coding=utf-8 -×-

from xmlrpclib import ServerProxy, Fault
from os.path import join, isfile, abspath
from SimpleXMLRPCServer import SimpleXMLRPCServer
from urlparse import urlparse
import sys

MAX_HISTORY_LENGTH = 6
SimpleXMLRPCServer.allow_reuse_address = 1

UNHANDLED = 100
ACCESS_DENIED = 200


class UnhandledQuery(Fault):
    """
    表示无法处理的查询异常
    """

    def __init__(self, message='Could not handle the query'):
        Fault.__init__(self, UNHANDLED, message)


class AccessDenied(Fault):
    """
    在用户试图访问未被授权的资源时引发的异常
    """

    def __init__(self, message='Access denied'):
        Fault.__init__(self, ACCESS_DENIED, message)


def inside(dir, name):
    """
    判断访问的目录是否有限制访问的目录，限制非法目录访问，比如/var/www/../data
    """
    dirs = abspath(dirs)
    name = abspath(name)
    return name.startswith(join(dirs, ''))


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
        try:
            print 'search local'
            return self._handle(query)
        except UnhandledQuery:
            # 添加到history，标记查找的深度
            history = history + [self.url]
            if len(history) >= MAX_HISTORY_LENGTH:
                raise
            print 'search other server'
            return self._broadcast(query, history)

    def hello(self, other):
        """
        认识其他节点
        """
        self.know.add(other)
        return 0

    def fetch(self, query, secret):
        """
        用于从节点下载数据
        """
        print 'server.fetch'
        if secret != self.secret:
            raise AccessDenied
        result = self.query(query)
        print 'result----', result
        # 把查询到的数据写到本地
        f = open(join(self.directory, query), 'w')
        f.write(result)
        f.close()
        return 0

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
            raise UnhandledQuery
        return open(name).read()

    def _broadcast(self, query, history):
        """
        内部时使用，用于将查询广播到其他已知节点
        """
        for other in self.know.copy():
            try:
                # 根据url创建远程节点的proxy，使用xml_rpc进行远程调用
                print 'search ----', other
                server = ServerProxy(other)
                print 'start query', other
                return server.query(query, history)
            except Fault, f:
                if f.faultCode == UNHANDLED:
                    pass
                else:
                    self.know.remove(other)
            except:
                # 说明该server已经不可用
                self.know.remove(other)
        # 如果在所有节点中没有找到，就返回空
        raise UnhandledQuery


def main():
    url, directory, secret = sys.argv[1:]
    node = Node(url, directory, secret)
    node._start()

if __name__ == '__main__':
    main()
