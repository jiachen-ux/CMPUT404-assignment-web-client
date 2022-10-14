#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
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

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

from ast import arg
import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib.parse as parse

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body
        
    def __str__(self):
        return f"{self.code}\r\n{self.body}"
    
class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        first_line = data.splitlines()[0]
        status_code = first_line.split()[1]
        return int(status_code)

    def get_headers(self,data):
        lines = data.splitlines()
        header_list = []
        for line in lines:
            if line == '':
                break
            header_list.append(line)
        header_str = '\r\n'.join(header_list)
        print(header_str)
        return header_str

    def get_body(self, data):
        lines = data.splitlines()
        i = lines.index('')
        body = lines[i:]
        bory_str = '\r\n'.join(body)
        return bory_str
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')
    
    def GET(self, url, args=None):
        code = 500
        body = ""
        parse_result = parse.urlparse(url)
        host = parse_result.hostname
        port = parse_result.port
        if port == None:
            port = 80
        # print('host', host, '\n', 'port', port,)
        
        self.connect(host, port)
        if parse_result.path == '':
            path = '/'
        else:
            path = parse_result.path
        
        send = f'GET {path} HTTP/1.1\r\nHost: {host}\r\nAccept: */*\r\nConnection: close\r\n\r\n'
        self.sendall(send)
        
        data = self.recvall(self.socket)
        
        code = self.get_code(data)
        body = self.get_body(data)
        
        self.close()
        print(data)
        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        code = 500
        body = ""
        parse_result = parse.urlparse(url)
        host = parse_result.hostname
        port = parse_result.port
        if port == None:
            port = 80
        # print('host', host, '\n', 'port', port,)
        
        if args != None:
            args = parse.urlencode(args)
        else:
            args = parse.urlencode('')
        
        self.connect(host, port)
        if parse_result.path == '':
            path = '/'
        else:
            path = parse_result.path
        
        send = f'POST {path} HTTP/1.1\r\nHost: {host}\r\nContent-Length: {len(args)}\r\nConnection: close\r\n\r\n{args}\r\n\r\n' #
        self.sendall(send)
        
        data = self.recvall(self.socket)
        
        code = self.get_code(data)
        body = self.get_body(data)
        
        self.close()
        print(data)
        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))
