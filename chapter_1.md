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

This will rise a http server sharing (listing) the contents of the directory where this command started. This is a call to class `SimpleHTTPRequestHandler`.

The `SimpleHTTPRequestHanler`  class is an implemetation from the `BaseHTTPRequestHandler` and implements some basic features like **GET** and **HEAD** HTTP methods among others.

To have a web server with the most used HTTP methods (GET, POST, PUT) we need to implement by ourselves it.

### Building a simple web server

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

Let's inspect the code.

First we import classes `HTTPServer`, the base stack of HTTP service and `BaseHTTPRequestHandler` for handling with the features and attributes of request like headers and response.

Define the class that will be he core of our application. 

The `BaseHTTPRequestHandler` has the `do_GET` method that handles with the **GET** request, and we are overwriting it to our speifiction.

The `self.send_response` will return the HTTP code for the operation. In this case, there is not process of anything, so it will allways answer **200** or **Ok**.

It's a good practice to write the specifications of the answer of application as `Content-Type` so the client knows what is expected to receive and how to handle this response. Since Python 3.3 is mandatory to close this workflow with `end_headers()` to avoid headers malformation. It adds a empty line to indicate the end of headers section.

In the end we write a response that is the output of request.

The last 2 lines we instantiate the `HTTPServer` class passing the address and the port that it will un. If we do not inform the address it will assume the external address (0.0.0.0). 

Running the code

To this server put up and running save this code in file as **example1-1.py**, open a terminal and run `python example1-1.py`.

To test it you can open a browser and try to connect to http://127.0.0.1:8080 or open a new terminal window and run `curl -v http://127.0.0.1:8080`.

Let's inspect the result of request made by curl.

```
$ curl -v http://192.168.1.79:8080
*   Trying 192.168.1.79:8080...
* Connected to 192.168.1.79 (192.168.1.79) port 8080 (#0)
> GET / HTTP/1.1
> Host: 192.168.1.79:8080
> User-Agent: curl/7.81.0
> Accept: */*
>
* Mark bundle as not supporting multiuse
* HTTP 1.0, assume close after body
< HTTP/1.0 200 OK
< Server: BaseHTTP/0.6 Python/3.10.12
< Date: Thu, 08 Feb 2024 13:00:19 GMT
< Content-Type: text/plain
<
Hello World!
* Closing connection 0
```

The fist block of information, lines starting with `>` are related to request (client part) and the second block, lines starting with `<` are related to response.

Now that we have an basic echoer http server let's try to add another method handler to our web server, **POST**.

### Adding a POST feature

To add **POST** method handler to our simple http server is as simple as was with **GET**, even because we will overwrite the `do_POST` method as we did with `do_GET`. The POST method implementation is preety much like the GET method but we will add to response the data sent with request.

Example 1-2

``` 
#!/usr/bin/env python

from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO


class HTTPRequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length'))
        body = self.rfile.read(content_length)

        self.send_response(200)
        self.end_headers()

        response = BytesIO()
        response.write(b'This is POST request. ')
        response.write(b'Received: ')
        response.write(body)

        self.wfile.write(response.getvalue())

        
if __name__ == "__main__":
    server = HTTPServer(('', 8080), HTTPRequestHandler)
    server.serve_forever()
#!/usr/bin/env python

```


