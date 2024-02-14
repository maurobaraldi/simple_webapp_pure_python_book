#!/usr/bin/env python

from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO


class HTTPRequestHandler(BaseHTTPRequestHandler 

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.wfile.write(b"Hello World!\n")
        self.end_headers 


if __name__ == "__main__":
    server = HTTPServer(('', 8080), HTTPRequestHandler)
    server.serve_forever()
