from socket import *

sock = socket()
sock.connect(('localhost', 12000))
socket.send('1')