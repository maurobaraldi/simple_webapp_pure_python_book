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

In the following example we will check if and reject the processing of request, answer HTTP status code 400 if this header isn’t defined.

Example 3-1

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

