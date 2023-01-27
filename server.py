#  coding: utf-8 
import socketserver
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        self.decoded_data = self.data.decode('utf-8')
        print ("Got a request of: %s\n" % self.data)

        # Types of responses
        OK_200 = "HTTP/1.1 200 OK\r\n"
        Moved_301 = "HTTP/1.1 301 Moved Permanently\r\n"
        NotFound_404 = "HTTP/1.1 404 Not Found\r\n\r\n"
        NotAllowed_405 = "HTTP/1.1 405 Method Not Allowed\r\n\r\n"

        # Gets path url from the decoded data
        url = self.decoded_data.split()[1]
        
        # Webpage display index.html on default
        if url[-1] == '/':
            url+='index.html'
        
        # Only handle 'GET' requests
        if self.decoded_data.split()[0] == "GET":
            
            # 404 if path does not exists
            if os.path.exists('./www'+ url):
                # check for html and css mime types
                if url.endswith('.html'):
                    res = b'Content-Type: text/html\r\n\r\n'
                    res += self.readFile(url)
                    self.request.sendall(bytearray(OK_200,'utf-8'))
                    self.request.sendall(res)
                elif url.endswith('.css'):
                    res = b'Content-Type: text/css\r\n\r\n'
                    res += self.readFile(url)
                    self.request.sendall(bytearray(OK_200,'utf-8'))
                    self.request.sendall(res)
                else:
                    url += '/'
                    self.request.sendall(bytearray(Moved_301,'utf-8'))
                    res = "Content-Type: text/plain\r\nLocation: " + url + "\r\n\r\n"
                    self.request.sendall(bytearray(res,"utf-8"))
            else:
                self.request.sendall(bytearray(NotFound_404,'utf-8'))
        else:
            # Status code 405, if requests is other than 'GET'
            self.request.sendall(bytearray(NotAllowed_405,'utf-8'))

    def readFile(self, path):    
        with open('./www'+ path,'r') as f:
            content = f.read()
        return bytearray(content,'utf-8')

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080
    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)
    
    server.serve_forever()
