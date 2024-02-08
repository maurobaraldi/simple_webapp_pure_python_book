#!/usr/bin/env python

from http.server import HTTPServer, BaseHTTPRequestHandler


class HTTPRequestHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Hello World!\n")

        
if __name__ == "__main__":
    server = HTTPServer(('', 8080), HTTPRequestHandler)
    server.serve_forever()
