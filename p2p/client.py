#! /usr/bin/env python
# -*- coding=utf-8 -*-

from xmlrpclib import ServerProxy, Fault
from cmd import Cmd
from random import choice
from string import lowercase
from server import Node, UNHANDLED
from threading import Thread
from time import sleep
import sys

HEAD_START = 0.1  # second
SECRET_LEN = 100


def randomStr(len):
    """
    生成指定长度的字符串
    """
    chars = []
    letters = lowercase[:26]
    while len > 0:
        len = len - 1
        chars.append(choice(letters))
    return ''.join(chars)


class Client1(Cmd):
    """
    Node基于文本的界面
    """

    def __init__(self, url, dirname, urlfile):
        """
        初始化Cmd
        随机生成秘钥
        启动服务器
        启动字符界面
        """
        print 'in'
        Cmd.__init__(self)
        self.secret = randomStr(SECRET_LEN)
        n = Node(url, dirname, self.secret)
        t = Thread(target=n._start)
        t.setDaemon(1)
        t.start()
        # 等待服务器启动
        sleep(HEAD_START)
        self.server = ServerProxy(url)
        for line in open(urlfile):
            line = line.strip()
            self.server.hello(line)

    def do_fetch(self, arg):
        "调用服务器的fetch方法"
        try:
            print 'do_fetch'
            self.server.fetch(arg, self.secret)
        except Fault, f:
            print f
            if f.faultCode != UNHANDLED:
                raise
            print 'Could not find the file ', arg

    def do_exit(self, arg):
        "退出程序"
        print
        sys.exit()

    do_EOF = do_exit  # 接收到EOF的时候也退出程序
    # 设置提示符
    prompt = '>'


def main():
    urlfile, directory, url = sys.argv[1:]
    print urlfile, directory, url
    print '---------'
    print dir()
    client = Client1(url, directory, urlfile)
    client.cmdloop()

if __name__ == '__main__':
    main()
