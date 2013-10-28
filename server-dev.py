import string, cgi, time
import sys
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from flask import Flask
from flask import request


app = Flask(__name__)


class MyHandler(BaseHTTPRequestHandler):

    def do_POST(self):
	global rootnode
	print "in do_POST"
	sys.stdout.flush()
	try:
	    ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
	    if cytype == 'multipart/formdata':
		query = cgi.parse_multipart(self.rfile, pdict)
		upfilecontent = query.get('upfile')
		print "filecontent", upfilecontent[0]
		sys.stdout.flush()
		self.send_response(200)
		return "file format"
	    #self.send_response(200)
	    elif ctype == 'application/x-www-form-urlencoded':
		print "in application/x-www-form-urlencoded"
		sys.stdout.flush()
        	length = int(self.headers.getheader('content-length'))
        	#postvars = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
		#return postvars
		post_body = self.rfile.read(length)
		self.send_response(200)
		return post_body	

	    #self.end_headers()
	    #upfilecontent = query.get('upfile')
	    #print "filecontent", upfilecontent[0]
	    #self.wfile.write("<HTML>POST OK. <BR><BR>")
	    #self.wfile.write(upfilecontent[0])

	    

	except: 
	    pass

@app.route('/',methods=['POST','GET'])
def main():
    print "hello"	
    try:
	print "in try in main"	
	print request.form['map']
	#return make_response( request.form['map'] )
	
	return request.form['map']
	#server = HTTPServer(('',80), MyHandler)
	print 'started httpserver...'
	#server.serve_forever()
    except KeyboardInterrupt:
	print 'shutting down'
	server.socket.close()


@app.route('/test',methods=['POST','GET'])
def test():
	print "in test Q___Q"
	return "this is test"



