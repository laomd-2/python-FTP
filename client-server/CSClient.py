from socket import *
from ..myutility.HKLPEnd import HKLPEnd

class CSClient(socket, HKLPEnd):
	"""client for client-server"""
	def __init__(self):
		"""create a TCP socket"""
		super(CSClient, self).__init__(AF_INET, SOCK_STREAM)
		pass


