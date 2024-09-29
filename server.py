#!/usr/bin/env python3
"""
License: MIT License
Copyright (c) 2023 Miel Donkers

Very simple HTTP server in python for logging requests
Usage::
    ./server.py [<port>]
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import subprocess

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        try:
            file_to_open = open(self.path[1:]).read()
            self.send_response(200)
        except:
            file_to_open = "File not found"
            self.send_response(404)
        self.end_headers()
        self.wfile.write(bytes(file_to_open, 'utf-8'))

    #def do_GET(self):
        #logging.info("GET-------- request,\nPath: %s\nHeaders:\n%s\n Server:%s\n Client:%s\n", str(self.path), str(self.headers),str(self.request.getsockname()[0]),str(self.client_address[0]))
        #self._set_response()
        ##self.wfile.write("GET*****request for {}".format(self.path).encode('utf-8'))
        #self.wfile.write(index.html.encode("utf-8"))
        #self.do_Client(self.client_address[0])
        
    def do_Client(self,client_ip):
        print("Client:",str(client_ip))
        mac=self.mac_from_ip(client_ip)
        #self.mac_from_ip(client_ip)
        print("Client Mac:",str(mac))
        
        
    def mac_from_ip(self,ip):
        arp_cmd=["cat", "/proc/net/arp"]
        proc = subprocess.Popen(arp_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (arp_cache, arp_err) = proc.communicate()
        arp_entries = arp_cache.decode().split("\n")
        for entry in arp_entries.copy():
        	if entry.startswith(ip):
        		#print(entry)
        		ip = entry.split()[0]
        		mac = entry.split()[3]
        		mac_if = entry.split()[5]
        		#print("IP:", ip)
        		#print("mac:",mac)
        		#print("mac_if:",mac_if)
        		return mac
        return None

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'))

        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=S, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
