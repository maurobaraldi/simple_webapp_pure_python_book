#!/usr/bin/env python

from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO


class HTTPRequestHandler(BaseHTTPRequestHandler 

    def do_HEAD(self):
        self.send_response(200)
        self.end_headers 

     def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.wfile.write(b"Hello World!\n")
        self.end_headers 

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length'))
        body = self.rfile.read(content_length)

        self.send_response(200)

        response = BytesIO()
        response.write(b'This is POST request. ')
        response.write(b'Received: ')
        response.write(body)

        self.wfile.write(response.getvalue())
        self.end_headers()

    def do_PUT(self):
        content_length = int(self.headers.get('Content-Length'))
        body = self.rfile.read(content_length)

        self.send_response(204)
        self.wfile.write(b"")
        self.end_headers()

    def do_DELETE(self):
        self.send_response(204)
        self.end_headers()
                            
        if __name__ == "__main__":
            server = HTTPServer(('', 8080), HTTPRequestHandler)
            server.serve_forever()


if __name__ == "__main__":
    server = HTTPServer(('', 8080), HTTPRequestHandler)
    server.serve_forever()

