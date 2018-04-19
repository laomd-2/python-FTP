from socket import *
import os
import struct
import json
serverName='172.18.32.225'
#serverName='172.19.112.112'
# serverName='192.168.155.2'
serverPort=12000

clientSocket=socket(AF_INET,SOCK_STREAM)		#创建套接字，AF_INET指示了地址簇，用于服务器与服务器之间的通信，底层用ipv4；SOCK_STREAM指明套接字类型，TCP套接字
clientSocket.connect((serverName,serverPort))	#建立TCP连接（三次握手）
print('Connecting to '+serverName+'......')

while 1:
	
	message=input()
	clientSocket.send(message.encode())
	if message=='q':
		break
	elif message=='file':
		fileinfo_size=struct.calcsize('128sl')
		buf=clientSocket.recv(fileinfo_size)				#接受数据包
		if buf:
			filename,filesize=struct.unpack('128sl',buf)	#解压数据包，得到文件名字和大小
			# fn=filename.decode().strip('\00')
			newFileName=os.path.join('./',filename.decode().strip('\00'))

			recv_size=0
			fp=open(newFileName,'wb')		#创建文件
			print('start receiving....'+str(filesize))
			ten_percent=int(filesize*0.1)
			number=0
			while not recv_size==filesize:					#把文件内容读出来
				if filesize - recv_size > ten_percent:
					data = clientSocket.recv(ten_percent)
					recv_size += len(data)
				else:
					data = clientSocket.recv(filesize - recv_size)
					recv_size = filesize
				fp.write(data)#把文件内容读进新创建的文件		
				os.system('cls')
				print(str(recv_size)+'/'+str(filesize))											
			fp.close()
			print('end receiving')
	elif message=='dir':
		tips_mes=clientSocket.recv(1024).decode()
		print(tips_mes)
		data=clientSocket.recv(2048)
		json_list=data.decode()		#解码字节流为json
		lists=json.loads(json_list)	#把接送解密为原来的列表
		for filename in lists:
			print(filename)
	elif message=='download':
		clientSocket.close()
