from socketserver import *
from ..myutility.HKLPEnd import HKLPEnd

class CSServer(BaseRequestHandler, HKLPEnd):
	"""server for client-server"""
	def handle(self):
		"""inherited from BaseRequestHandler, deal with main logic of CSServer"""
		pass

if __name__ == '__main__':
	server = ThreadingTCPServer(("", 12000), CSServer)
	server.serve_forever()
