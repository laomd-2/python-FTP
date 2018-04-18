class HMBPServer(object):
	"""docstring for KMBPServer"""
	def __init__(self, port):
		"""port:端口号"""
		pass

	def getClientSocket(self):
		"""返回当前用户套接字"""
		pass

	def sendList(self,client_socket):
		"""列出文件目录，client_socket:客户套接字"""
		pass

	def sendFile(self,client_socket,file_name):
		"""发送文件给请求方"""
		pass

	def recvFile(self,client_socket,file_name):
		"""接受文件"""
		pass

