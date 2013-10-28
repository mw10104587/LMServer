import string, cgi, time
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from flask import Flask

app = Flask(__name__)


class MyHandler(BaseHTTPRequestHandler):

    def do_POST(self):
	global rootnode
	try:
	    ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
	    if cytype == 'multipart/formdata':
		query = cgi.parse_multipart(self.rfile, pdict)
		upfilecontent = query.get('upfile')
		print "filecontent", upfilecontent[0]
		return "file format"
	    #self.send_response(200)
	    elif ctype == 'application/x-www-form-urlencoded':
        	length = int(self.headers.getheader('content-length'))
        	#postvars = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
		#return postvars
		post_body = self.rfile.read(length)
		return post_body	

	    #self.end_headers()
	    #upfilecontent = query.get('upfile')
	    #print "filecontent", upfilecontent[0]
	    #self.wfile.write("<HTML>POST OK. <BR><BR>")
	    #self.wfile.write(upfilecontent[0])

	    

	except: 
	    pass

@app.route('/',methods=['POST'])
def main():
    try:
	server = HTTPServer(('',80), MyHandler)
	print 'started httpserver...'
	server.serve_forever()
    except KeyboardInterrupt:
	print 'shutting down'
	server.socket.close()
@app.route('/test')
def test():
	return "this is test"


if __name__ == '__main__':
    app.run()

