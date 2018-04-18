from socketserver import *

class Tracker(BaseRequestHandler):
	def handle(self):
		pass

	def _register(self, client_socket):
		"""register client socket to client set and return neighbors of client socket"""
		pass