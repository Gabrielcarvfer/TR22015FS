#!/usr/bin/env python
#import BaseHTTPServer
#from CGIHTTPServer import CGIHTTPRequestHandler
from websock import websock
from socketUDP import udpsock_broadcaster, udpsock_listener
import threading
def main():
	try:

		#server_address = ('', 8080)

		#server = BaseHTTPServer.HTTPServer
		#handler = CGIHTTPRequestHandler
		#handler.cgi_directories = ['/cgi-bin']

		#httpd = server(server_address, handler)
		#httpd.serve_forever()
		server = threading.Thread(target=websock)
		server.start()
		print 'Started httpserver...'

		broad = threading.Thread(target=udpsock_broadcaster)
		broad.start()
		print 'Started udp broadcaster...'

		listen = threading.Thread(target=udpsock_listener)
		listen.start()


	except KeyboardInterrupt:
		print '^C received, shutting down server'
		#server.socket.close()

if __name__ == '__main__':
	main()
		
