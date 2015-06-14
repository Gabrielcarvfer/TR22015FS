import cgi, string, time, os, os.path
from os import curdir, pardir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

class WebHandler (BaseHTTPRequestHandler):
	def do_GET(self):
		try:
			if self.path.endswith(".html"):
				f = open(curdir + sep + self.path)
				self.send_response(200)
				self.send_header('Content-type', 'text/html')	
				self.end_headers()
				self.wfile.write(f.read())
				f.close()
				return
			if self.path.endswith(".esp"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				self.wfile.write("Hey dude,\n" + str(time.localtime()[0]));
				return
			return
		except IOError:
			self.send_error(404, 'File Not Found: %s', self.path)
	def do_POST(self):
		global rootnode
		try:
			print "receiving file"
			form = cgi.FieldStorage()
			print form
			ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
			if ctype == 'multipart/form-data':
				print "Okey dokey"
				print "parsing file"
				query=cgi.parse_multipart(self.rfile, pdict)
			self.send_response(301)

			self.end_headers()
			upfilecontent = query.get('upfile')
			"""print "uploading file"""
			"""print "filecontent", upfilecontent[0]"""
			self.wfile.write("<HTML>POST OK.<BR><BR>")
			"""self.wfile.write(upfilecontent[0])"""

			fout = open(os.path.join(pardir, 'uploads', form['upfile'].filename), 'wb')
			print os.path.join(partir, 'uploads', form['upfile'].filename)
			fout.write(upfilecontent);
			fout.close();

		except:
			pass


def main():
	try:
		server = HTTPServer(('', 80), WebHandler)
		print 'started httpserver...'
		server.serve_forever()
	except KeyboardInterrupt:
		print '^C received, shutting down server'
		server.socket.close()
if __name__ == '__main__':
	main()
		