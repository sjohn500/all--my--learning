## Lesson 4: HTTP Requests and Responses

Think of it as a conversation.
Client (Browser/App)
        │
        │ Request
        ▼
Backend Server
        │
        │ Response
        ▼
Client

# Anatomy of an HTTP Request
An HTTP request has five important parts.
Method
URL
Headers
Body
Query Parameters (sometimes)

1. METHOD = the method tells the server what action you want
Example:
GET/users
meaning:
   Give me all users.
Another:
POST/users
meaning:
  create a new user.


2. URL = the URL tells the server which resource you want.
Example:
GET/users
The resource is:
users
Another example:
GET/produts
Resource:
products

3. HEADERS:= Headers contain extra information about the request.
Think of headers like the information written on the outside of a package before it's delivered.

Example:
GET /users

Content-Type: application/json

Authorization: Bearer abc123

Accept: application/json

Content-Type = Tells the server what format the body is in.
Example:
Content-Type: application/json
Meaning:
i'm sending JSON.
Accpet := Tells server what format the client wants back.
Accept: application/json
Meaning:
please respond with JSON.


Authorization

Used when a user is logged in.

Example:
Authorization: Bearer eyJhb...

This is how the server knows who is making the request.

We'll learn this in detail when we study authentication.

