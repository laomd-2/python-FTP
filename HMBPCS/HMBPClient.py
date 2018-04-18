import socket
import sys
import json
import struct
import os
class HMBPClient(object):
	"""docstring for Peer"""
	def __init__(self, is_last=True):
		"""is_last：是否建立持续连接"""
		self.is_last=is_last;
		self.help_dic={'help':'get the help information','dir':'list the orders','quit':'quit the client','download':'download file in the server'}
		try:
			self.msocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		except socket.error:
			print("Socket create failed!")
			sys.exit(1)
	def connect(self,ip_addr,port):
		"""建立tcp连接，ip_addr:服务器ip地址，port:端口号"""
		try:
			self.msocket.connect((ip_addr,port))
		except socket.error:
			print("Can't connect to "+ip_addr)
			sys.exit(1)
		else:
			print("Connect to "+ip_addr+" successfully!")

	def receive(self,bytes):
		"""接受客户端发过来的字节流并解码为原来的类型返回给客户端"""
		return self.msocket.recv(bytes).decode()
		

	def dir(self):
		"""获取文件目录，
		返回文件名字符串列表"""
		tips_mes=client1.receive(1024)
		print(tips_mes)
		json_list=client1.receive(1024)	#解码字节流为json
		lists=json.loads(json_list)	#把接送解密为原来的列表
		return lists

	def download(self,absolute_path='./',file_name='receive_file'):
		"""下载文件file_name到absolute_path，返回文件对象，没有该文件就抛异常"""
		#交给服务器查找是否有该文件
		self.ask(file_name)
		fileinfo_size=struct.calcsize('128sl')
		buf=self.msocket.recv(fileinfo_size)				#接受数据包
		if buf:
			filename,filesize=struct.unpack('128sl',buf)	#解压数据包，得到文件名字和大小
			newFileName=os.path.join(absolute_path,filename.decode().strip('\00'))
			recv_size=0
			fp=open(newFileName,'wb')		#创建文件
			print('start receiving....'+str(filesize))
			ten_percent=int(filesize*0.1)
			number=0
			while not recv_size==filesize:					#把文件内容读出来
				if filesize - recv_size > ten_percent:
					data = self.msocket.recv(ten_percent)
					recv_size += len(data)
				else:
					data = self.msocket.recv(filesize - recv_size)
					recv_size = filesize
				fp.write(data)#把文件内容读进新创建的文件		
				os.system('cls')
				print(str(recv_size)+'/'+str(filesize))											
			fp.close()
			print('end receiving')
		

	def upload(self,absolute_path='./',file_name=''):
		"""上传文件，absolute_path：文件所在绝对路径，file_name:文件名字，返回是否上传成功"""
		
		filepath='E:/new/'+file_name
		print(filepath)
		file_size=os.stat(filepath).st_size     #os.stat() 方法用于在给定的路径上执行一个系统 stat 的调用,显示文件filepath信息
		fhead=struct.pack('128sl',os.path.basename(filepath).encode(),file_size) #
		#struct.pack用于将Python的值根据格式符，转换为字符串（因为Python中没有字节(Byte)类型，可以把这里的字符串理解为字节流，或字节数组）
		ten_percent=int(file_size*0.1)
		self.msocket.send(fhead)		#发送文件头信息，包括名字和大小
		fp=open(filepath,'rb')
		while 1:
			data=fp.read(ten_percent)
			if not data:
				print('send over')
				break
			self.msocket.send(data)     #发送文件内容	

	def ask(self,ask_inf):
		"""发送请求给服务端"""
		self.msocket.send(ask_inf.encode())

	def shutDownConnect(self):
		self.msocket.close()
		exit(1)

	def showHelp(self):
		for order,function in self.help_dic.items():
			print("%-10s"%order,function)

if __name__ == '__main__':
	client1=HMBPClient()
	client1.connect('172.18.32.225',12000)
	while 1:
		print('HMBPServer:>',end='')
		ask_inf=input()
		client1.ask(ask_inf)
		if ask_inf.strip()=='help':
			client1.showHelp()
		elif ask_inf.strip()=='quit':
			client1.shutDownConnect()
		elif ask_inf.strip()=='dir':
			lists=client1.dir()
			for file_name in lists:
				print(file_name)
		elif ask_inf.strip()=='download':
			file_name=input('Please input the filename:')
			# absolute_path=input('\nPlease input the absolute path you want to save this file:',end='')
			client1.download('./',file_name)
		elif ask_inf.strip()=='upload':
			file_name=input('Please input the file name:')
			client1.upload('./',file_name)







		