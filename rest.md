## Lesson 2: REST
 # what is REST?
 REST stands for:
   REpresentational state Transfer
   
REST is a set of rules and best practices for designing APIs so they are consistent and easy to understand.
A Complete REST API

Imagine you're building an online bookstore.

| Action        | Method | Endpoint   |
| ------------- | ------ | ---------- |
| Get all books | GET    | `/books`   |
| Get one book  | GET    | `/books/8` |
| Add a book    | POST   | `/books`   |
| Update a book | PUT    | `/books/8` |
| Delete a book | DELETE | `/books/8` |

# whate Gose in the URL?
 A URL often has two parts
 /users/5
 1. /users --> the resource(collection)
 2. --> the specific item(ID)

 REST Summary 

 | Method | Endpoint   | Meaning       |
| ------ | ---------- | ------------- |
| GET    | `/users`   | Get all users |
| GET    | `/users/5` | Get user 5    |
| POST   | `/users`   | Create a user |
| PUT    | `/users/5` | Update user 5 |
| DELETE | `/users/5` | Delete user 5 |


