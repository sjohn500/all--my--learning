## what is API?
 API stand for Application Programming Interface.
     an API is a messenger between two programs
for example:
you
 |
 phone App
   |
 API
   |
Database

The API recevies your request, checks it, gets the data, and sends it back.

An API is a layer that allows one application to communicate with another. In a web application, the API usually sits between the client (browser or mobile app) and the backend logic/database.

# what is a backend?
 the backend is everthing users don't see
 it usually contains:
 Client
  |
Backend Server
   |
Database

example: 

Browser

↓

Node.js Server

↓

PostgreSQL



# What happens when you log into Facebook?
You enter

Email

Password

↓

POST /login

↓

Server checks database

↓

Correct?

↓

Yes

↓

Returns your account

API Endpoints

an endpoint is simply a URL that performs a specific action.
Example:
GET /users

GET /products

POST /login

POST /register

PUT /users/5

DELETE /users/5

# HTTP Method
1. GET = Gets data, Get never  creates data. it only reads
2. POST = creates new data the server saves it
3. PUT = updates existing data
4. DELETE = Delete data.

# JSON
almost every API senda and receives JSON
JSON stands for :
JavaScript Object Notation

JSON is used to exchange data between the client and the server.

JSON
{
    "name":"John",
    "age":24,
    "country":"Nigeria"
}


Notice:

keys are in quotes
strings are in quotes
numbers are not

JSON Array
[
    {
        "name":"John"
    },
    {
        "name":"Sarah"
    }
]

Request is what the client sends.
GET/ users
or POST/login

Response the sever sends back a respondse
Example:
{
    "message":"Login successful"
}
or 

{
    "error":"Wrong password"
}

STATUS CODE
| Code | Meaning               |
| ---- | --------------------- |
| 200  | OK                    |
| 201  | Created               |
| 400  | Bad Request           |
| 401  | Unauthorized          |
| 403  | Forbidden             |
| 404  | Not Found             |
| 500  | Internal Server Error |
