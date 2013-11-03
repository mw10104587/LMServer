import string, cgi, time
import sys
import json
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from flask import Flask
from flask import request

from graph import *
from findPeculiarAngles import *
from find_subgraph import *
from isomorphism import *
from find_neighbor import *
from get_like import *


app = Flask(__name__)
g_query, g_map, nodes = None, None, []

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
def foo():
    print "Rcv Req"   
    try:
        # path = request.form['path']
        # path = [(0, 0), (3,5), (320,568)]
        # g_query = create_user_graph(path)
        
        # Find Isomorphism Subgraph
        

        # output = data
        # data = sub_graph(g_query, g_map)
        # data_string = json.dumps(data[len(data)-1])
        data = get_like(nodes)
        data_string = json.dumps(data)

        print "Get Data..."
        print data_string

        return data_string
        #server = HTTPServer(('',80), MyHandler)
        # print 'started httpserver...'
        #server.serve_forever()
    except KeyboardInterrupt:
        print 'shutting down'
        server.socket.close()


@app.route('/test',methods=['POST','GET'])
def test():
    print "in test Q___Q"
    return "this is test"


if __name__ == '__main__':
    print "Connecting..."
    # [g_query, g_map] = initAll()
    nodes = init_like()
    print "Connected"
    app.run(host='0.0.0.0')

