# Chapter 3 - Headers and Routing

In the previous chapters we saw about the HTTP protocol and concepts around it, and basic features from BaseHTTPRequestHandler class from http lib. With that we have all that we need to start a very web basic application using just Python. Now let’s add some power on this engine and increase its potency!

## Headers 

The headers are the metadata of the request, all the information you need to know or inform, about from request or the answer that is not the body, you will found in headers. You may make requests or have responses without data, but it’s not usual without, any, headers. Even when you do not specify the headers explicitly, there are some basic headers that are sent by the client app or lib.

### The essential headers

When we make a request, using curl, to a web server there are some headers that automatically always send with the request.

Example:

```
$ curl -v http://192.168.1.79:8080
Trying 192.168.1.79:8080...
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
```

As we can see at least `method `, `host `, `user-agent` and `accept` are always sent with basic request with curl. All these headers could be overwritten as any other could be added.

For the response we may have the same with `status_code`, `server`, `date` and `content-type`. And the rule is the same for response.

## Headers in request

It is possible, and it is a good practice, to perform some validations of the request in headers. It can save some time and resource of processing.

Example: The API endpoint expects a `content-type` of value `application/json` but the request is defined as `text/plain`or even isn’t defined. You do not need to load the data to check and validate it.

It doesn't means that the body doesn't need to be validated after, but this could be an enforcement advisory that this is the expected MIME type of content according to API definition.

The object that store all headers sent by the request is the [`headers`](https://docs.python.org/3/library/http.server.html#http.server.BaseHTTPRequestHandler.headers) dict.

In the following example we will check if and reject the processing of request, answer HTTP status code 400 if this header isn’t defined.

Example 3-1

``` 
#!/usr/bin/env python

from http.server import HTTPServer, BaseHTTPRequestHandler

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

        def do_GET(self):
            if self.headers.get('API-Key'):
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'Hello, world!')
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'Missing header "API-Key"')

if __name__ == "__main__":
    server = HTTPServer(('', 8080), SimpleHTTPRequestHandler)
    server.serve_forever()
```
As we can see there is a validation to check if a header was sent in the request (didn’t validated the value yet), and the application returned the Bad Request status code (400) as it is absent. This should be the status code, because the request wasn’t in accordance with the definition for that endpoint.

This could be the example of curl to test. The request part will be omitted because it doesn’t matter for the context.

$ curl -v -H "Content-Type: text/plain" http://127.0.0.1:8080
…
* Mark bundle as not supporting multiuse
* HTTP 1.0, assume close after body
< HTTP/1.0 400 Bad Request
< Server: BaseHTTP/0.6 Python/3.8.10
< Date: Tue, 20 Feb 2024 18:34:52 GMT
< 
Missing header "API-Key"
* Closing connection 0

### Headers in response

In order To add headers to response we should use the method [`send_headers`](https://docs.python.org/3/library/http.server.html#http.server.BaseHTTPRequestHandler.send_header), passing the key and the value of header as parameter, that appends this header to an internal buffer (like a collection of headers) and it is sent with the response body after the call of  [`end_headers`](https://docs.python.org/3/library/http.server.html#http.server.BaseHTTPRequestHandler.end_header).

One common example of use of headers in response is in the pagination of of content in APIs. Each request can return a limited amount of registries, but the query that originated that request may return mor values than it is designed to return. So, application adds a header that specify which set of registries, page, is that one, and so we can run the next request from the next page.

In the example below the application will add a custom header to response.

Example 3-2

```
from http.server import HTTPServer, BaseHTTPRequestHandler


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

        def do_GET(self):
            if self.headers.get('API-Key'):
                self.send_response(200)
                self.send_header("Custom-header","Test")
                self.end_headers()
                self.wfile.write(b'Hello, world!\n')
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'Missing header "API-Key"\n')

if __name__ == "__main__":
    server = HTTPServer(('', 8080), SimpleHTTPRequestHandler)
    server.serve_forever()

```
This should be the response

```
$ curl -v -H "API-Key: text/plain" http://127.0.0.1:8080
…
* Mark bundle as not supporting multiuse
* HTTP 1.0, assume close after body
< HTTP/1.0 200 OK
< Server: BaseHTTP/0.6 Python/3.8.10
< Date: Tue, 20 Feb 2024 19:27:12 GMT
< Custom-header: Test
< 
Hello, world!
* Closing connection 0
```

Although HTTP headers are very important and useful they are simple to build and handle with. At this point, the decision to build something simple using standard **http** lib and use a mature solution (web framework) comes. 

Handle with headers are pretty simple but as soon the solution become more complex more features you may need to add to headers, combining also with the next topic of this chapter, Routing.

## Routing

Design a good routing engine is a really challenging endeavor. The rules for the using aren’t much complex, even though it follows a standard commonly known as URL or URI (Uniform Resource Identifiers).

We won’t approach advanced concepts of routing like regex, right now. This chapter will focus on present a simple solution of how to handle with routing in with our simple  examples. In the appendix XXX - Other Examples, you can find and example of a routing engine with regex.

### Basic URI

The URI is a part of the request, and can be accessed by the attribute path. In the following example we can see a simple way to handle the routing.

Example 3-3

```
from http.server import HTTPServer, BaseHTTPRequestHandler


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

        def do_GET(self):
            if self.path == “/foo”:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b’Endpoint: /foo\n')
            elif self.path == “/bar”:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b’Endpoint: /bar\n')
            else:
                self.send_response(404)
                self.end_headers()

if __name__ == "__main__":
    server = HTTPServer(('', 8080), SimpleHTTPRequestHandler)
    server.serve_forever()
```

The `self.path` compares the value to `/foo` because the path starts from `/`,  so everything in the `self.path`, including the query, should be parsed by the application. If we do not set the response for the 404, it will send an empty reply from server.

The next example will handle with the query from the URI.

Warning: This is not a very elegant solution and was done consciously. In the end of the appendix, there will be a more elegant solution to parse routes and query.

```
from http.server import HTTPServer, BaseHTTPRequestHandler


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

        def do_GET(self):
            if self.path.startswith(“/foo”):
                if self.path.contains(“?”):
                    query = self.path.split(“?”)[1]
                    query = [i.split(“=“) for i in query.split(“&”)]
                    print(query)
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b’Endpoint: /foo\n')
            elif self.path == “/bar”:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b’Endpoint: /bar\n')
            else:
                self.send_response(404)
                self.end_headers()

if __name__ == "__main__":
    server = HTTPServer(('', 8080), SimpleHTTPRequestHandler)
    server.serve_forever()
```

As we are creating an application, from scratch, using the HTTP stack library, some situations are not already resolved so need to be created, like the URI query parameters.

One painful situation here would be to have multiples methods associated to an URI, that we will need to, using this approach, rewrite some part of the logic to other methods. But the purpose here is to write simple applications and will not complicate the scenarios.

## Conclusion

