import BaseHTTPServer
from CGIHTTPServer import CGIHTTPRequestHandler

def main():
	try:

		server_address = ('', 80)

		server = BaseHTTPServer.HTTPServer
		handler = CGIHTTPRequestHandler
		handler.cgi_directories = ['/cgi-bin']

		httpd = server(server_address, handler)
		httpd.serve_forever()
		print 'started httpserver...'

	except KeyboardInterrupt:
		print '^C received, shutting down server'
		server.socket.close()

if __name__ == '__main__':
	main()
		
