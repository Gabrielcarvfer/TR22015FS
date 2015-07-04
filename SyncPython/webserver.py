#!/usr/bin/env python
from websock import websock
from sockthread import startUDPServer
import thread
def main():
	try:
		peer_dict = {}

		#server = threading.Thread(target=websock)
		thread.start_new_thread( websock, () )
		print 'Started httpserver...'

		#thread.start_new_thread( startUDPServer, (peer_dict) )
		startUDPServer(peer_dict)
		print 'Started udp broadcaster...'



	except KeyboardInterrupt:
		print '^C received, shutting down server'
		#server.socket.close()

if __name__ == '__main__':
	main()
		
