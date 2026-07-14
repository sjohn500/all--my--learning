## Lesson 3: JSON (JavaScript Object Notation)

Almost every REST API uses JSON to send and receive data.

Think of JSON as the language that the client and server use to communicate.

for example:
Browser
   │
   │ JSON
   ▼
Backend API
   │
   │ JSON
   ▼
Database

A Simple JSON Object
```JSON
{
  "name": "John",
  "age": 24,
  "isStudent": true
}
```
Let's break it down:

{} means an object.
"name" is a key.
"John" is its value.
Keys are always strings, so they are in quotes.
Values can be different types.
# JSON vs JavaScript Object
Because JSON stands for JavaScript Object Notation, people often think they are the same. They are not.

```javaScript
const user = {
  name: "John",
  age: 24
};
```
```JSON
{
  "name": "John",
  "age": 24
}

```


