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

To add **POST** method handler to our simple http server is as simple as was with **GET**, even because we will overwrite the `do_POST` method as we did with `do_GET`. The POST method implementation is preety much like the GET method but we will add to response the data sent by request.

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
        response.write(b'Received: ')
        response.write(body)

        self.wfile.write(response.getvalue())

        
if __name__ == "__main__":
    server = HTTPServer(('', 8080), HTTPRequestHandler)
    server.serve_forever()

```

The POST request always send the hearder `Content-Length` so the HTTP server could handle with the size of data, whether for reading or validation. This value is the total in bytes of the data sent by request and can be used by `rfile` buffer object to read this data. Right after the process of the data, we prepae the haders for response. Even if we do not add any infoto headers, we need to finish the headers workflow, with `end_headers`.

Next step is build the response message (response body) and it could be done creating a buffer and write all the data on it. The last part is write the response with content of buffer.

To run a request to this example using curl use this:

`$ curl -v -H "Content-Type: text/plain" --data "Hello World" http://127.0.0.1:8080`

And this should be the result:

```
*   Trying 127.0.0.1:8080...
* Connected to 127.0.0.1 (127.0.0.1) port 8080 (#0)
> POST / HTTP/1.1
> Host: 127.0.0.1:8080
> User-Agent: curl/7.81.0
> Accept: */*
> Content-Type: text/plain
> Content-Length: 9
> 
* Mark bundle as not supporting multiuse
* HTTP 1.0, assume close after body
< HTTP/1.0 200 OK
< Server: BaseHTTP/0.6 Python/3.10.12
< Date: Thu, 08 Feb 2024 17:22:50 GMT
< 
* Closing connection 0
This is POST request. Received: Hello World
```

This example uses a Mime type used in example is `text/plain`. 

In this example the response code is 200, just for example purposes and because there is nothing been created in server.

There is more data formats to handle with a POST request, but it will be aproched in chapter XXX - Templating and Forms.

### Adding a PUT method 

The difference between POST and PUT is that PUT is idempotent, therefore the result code should be 201 when creating a new resource on system or one between 200 and 204, and the criteria was already seen in Chapter 1.

As this is our first implementation of a PUT method it will be pretty much like the POST on but just answering the different response code. In the end of chapter we will see a rudimentary resource persistence engine with all methods seen in this chapter.

Example 1-3

``` 
#!/usr/bin/env python

from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO


class HTTPRequestHandler(BaseHTTPRequestHandler):

    def do_PUT(self):
        content_length = int(self.headers.get('Content-Length'))
        body = self.rfile.read(content_length)

        self.send_response(204)
        self.end_headers()

	self.wfile.write(b“”)

if __name__ == "__main__":
    server = HTTPServer(('', 8080), HTTPRequestHandler)
    server.serve_forever
```

And the result of a request to this endpoint should be like this.


```
* Trying 127.0.0.1:8080...
* Connected to 127.0.0.1 (127.0.0.1) port 8080 (#0)
> PUT / HTTP/1.1
> Host: 127.0.0.1:8080
> User-Agent: curl/7.81.0
> Accept: */*
> Content-Type: text/plain
> Content-Length: 16
> 
127.0.0.1 - - [13/Feb/2024 05:44:40] "PUT / HTTP/1.1" 204 -
* Mark bundle as not supporting multiuse
* HTTP 1.0, assume close after body
< HTTP/1.0 204 No Content
< Server: BaseHTTP/0.6 Python/3.10.12
< Date: Tue, 13 Feb 2024 05:44:40 GMT
< 
* Closing connection 0
```

### Adding a DELETE method

DELETE method is the last one of the CRUD concept to be implemented and it behaves like the PUT method, but removing the resource  from persistence engine. It has also specific response codes each situation. 200 and 204 works likewise the PUT method, but it has the “special” status code, the 202. According to RFC 9110:

 ```
The 202 (Accepted) status code indicates that the request has been accepted for processing, but the processing has not been completed. The request might or might not eventually be acted upon, as it might be disallowed when processing actually takes place. There is no facility in HTTP for re-sending a status code from an asynchronous operation.

The 202 response is intentionally noncommittal. Its purpose is to allow a server to accept a request for some other process (perhaps a batch-oriented process that is only run once per day) without requiring that the user agent's connection to the server persist until the process is completed. The representation sent with this response ought to describe the request's current status and point to (or embed) a status monitor that can provide the user with an estimate of when the request will be fulfilled.
```

This status code isn’t much seen in usual CRUD systems and could be used in scheduling system that performs maintenance actions periodically or in asynchronous operations. One example of use is in cascade deletion of resources, asynchrony, in Kubernetes. The apiserver answers 202 for the clients and then all the process occurs in background.

The implementation could be much more like the GET than the PUT, because the URI should be the identifier of the resource.

Example 1-4

``` 
#!/usr/bin/env python

from http.server import HTTPServer, BaseHTTPRequestHandler


class HTTPRequestHandler(BaseHTTPRequestHandler):

    def do_DELETE(self):
        self.send_response(204)
        self.end_headers()
                            
        if __name__ == "__main__":
            server = HTTPServer(('', 8080), HTTPRequestHandler)
            server.serve_forever()
```

### Adding HEAD, CONNECT, OPTION and TRACE methods

The HEAD method is almost the same behavior and implementation than GET but without the body in answer, just the headers. As the HEAD is used, most of the time, for testing the availability of resource, we may just use the same implementation of GET, without the response body.

The response should be 200 when it is found, or 404 when it isn’t. It is ver common to use HEAD as a health check purpose.

We can just reuse the do_GET method just renaming to do_HEAD deleting the line self.wfile.write(b"Hello World!\n").

CONNECT, OPTION and TRACE methods are specifics methods that will discussed and reviewed in chapter 12 - Advanced Methods.


## Wrapping all together 

We have one isolated example for each method described here, but HEAD. Let’s build now an example with all methods together. This example is the union of all the examples in one class that will response to each request method.

After the example you may find a list of requests using another excellent resource from standard library, the urllib.

Example 1-5


```
```


# Conclusion

In this chapter you found the basic structure of BaseHTTPRequestHandler class and how to start exploring it. With these basic examples you can start your very first application pure Python based, in any environment.

In the next chapter we will start with some basic validation in the headers level and add look for a routing handle feature.
