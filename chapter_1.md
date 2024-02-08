# Simple HTTP Server

The standard library is, in my opinion, the second strongest point of Python. The fisrt one is the community, thates expected, maintain this very valuable lib.

The http lib is common criticized because becausei is hard to understand and use. But the problem isn't the lib, but the HTTP stack per se. Despite it is designed to be simple, it expect from the developer to have knowledge fo some concepts to work properly.

It is pretty common to see a lot of external libraries to handle with http resources and the most common is the requests[1] to handle wih the http client part in a easier way. Neverthless this faciliy (sometimes known as syntnax sugar) comes with drawbacks. And in this case the bad part here is the dependency of a external lib. There is a sort of points to discuss the advanages and disadvantages of use external libs in project, but the only points I would like to enlight here are the security and the dependency of a external lib to solve simpler problems.

Well, returning to the http lib, it has 4 modules:

- client: that is the base for the **urllib.request** lib.
- server: which we will see extensively in this book and is based on **socketsrver**
- cookies: to handle with cookies.
- cookiesjar: that provides persistence to cookies.

## Simple HTTP Request Handler

Perhaps you already saw anytime around the internet that the simplest way to put an http server up and running in Python, with one line is the following snippet:

```python -m http.server 8000```

This will rise a http server sharing (listing) the contents of the directory where this command started. This is a call to class `SimpleHTTPRequestHandler`

The `SimpleHTTPRequestHanler`  class is an implemetation from the `BaseHTTPRequestHandler` and implements some basic features like **GET** and **HEAD** HTTP methods among others.

To have a web server with the most used HTTP methods (GET, POST, PUT) we need to implement by ourselves it

## Building a simple web server

The `BaseHTTPRequestHandler` has the basic methods already implemented and you can overhide the method if you want to improve or change any behaviour of the current implementation.

Here is the most basic implementation of a web server with the GET method.

Example 1-1

``` 
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
```

To this server put up and running save this code in file as **example1-1.py**, open a terminal and run `python example1-1.py`.

To test it you can open a browser and try to connect to http://127.0.0.1:8080 or open a new terminal window and run `curl -v http://127.0.0.1:8080`.


