# Itroduction

This chapter is a guide for nomenclature of terms, acronyms and description of some concepts that will be covered here.

## Disclaimer 

There is a lot of solutions stable, secure and free, for web servers tou se in productive environments. If you are looking for a solution like this I would suggest you to lookfor one of he follwing projects.

Apache

NGinx

HAProxy

Lwan

## Basic Concepts

### HTTP Protocol

The HTTP is an acronym for Hypertext Transfer Protocol. It is an application layer protocol designed for the traffic of hypertext documents including hyperlinks through a TCP/IP based network. There was a lot of improvements and changes since your first public version 1.0 in 1996, and then evolved to versions 1.1 in 1997, 2.0 in 2015 and then to last version, 3.0 presented in June of 2022.

During the time the changes and features turned it more secure, resilient and accessible. One of the main features was the ability communicate through secure channels using SSL (future replaced by TLS and it’s newer versions) in version 2 and lower latency in version 3 with QUIC protocol.

There are very useful information about HTTP protocol and all your ecosystem in their RFCs, that could be found in Reference area in the end of book

### HTTP Server

Mostly known as web server it is an application, and sometimes an underlying hardware, that acts answering the requests (server side) made by the applications acting as client. These applications could be web browsers, or other applications build on top of the HTTP stack. Nowadays the most common scenario found in web applications is to have an application running on top of HTTP server, that interacts with the server through an another application called WSGI or ASGI.

### Web Application

Web applications or web apps is any application that runs on a HTTP server. In Wikipedia the term web resource is associated to web application and this is the description:

“Web resource is any identifiable resource (digital, physical, or abstract) present on or connected to the World Wide Web. Resources are identified using Uniform Resource Identifiers (URIs). In the Semantic Web, web resources and their semantic properties are described using the Resource Description Framework (RDF).”

A web app could be rest api that expose an interface from a database, a web service running in REST architecture design, SOAP or RPC protocols, a template rendering content since a simple static content application until an AJAX application running in client browser that connects to backend to communicate with the information.

