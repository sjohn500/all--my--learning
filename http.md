## what is HTTP?

the full meaning of HTTP is HYPERTEXT TRANSFER PROTOCOL

EXPLAINATION :
let me build you a vilsual story:
you(BROWSER):Sitting at the table hungry for a webpage
(HTTP): the waiter that carries your order & food 
server(KICHEN): stores & prepares the webpage for you

## how it actually works - step by step

step 1: ----REQUEST:
when you type google.com--> your browser send a REQUEST:"Hey server, please give me the google homepage!"

step 2: ----SERVER GETS IT
The server hears your oder, goes to find the page files(HTML,images, etc) and prepares them.

step 3: ----RESPONSE
server sends back a RESPONSE: a statue code (like 200 Ok = "here's your food!") + the actual webpage.

step 4: ----YOU SEE THE PAGE
your browser reads the HMTL & CSS files and draws the webpage on your screen,Done!

## HTTP status codes -- the waiters reply

# 1
200 ok : Here's your food (DONE)
# 2
301 Redirect: we moved! Go here(reloading)
# 3
404 Not found: that's dish is'nt here(not found)
# 4
500 Server Error: kitchen's on fire($)

# HTTP VS HTTPS -- what's the S for

## HTTP:
LIKE SENDING A POSTCARD - anyone can read it (<!>)

## HTTS:
LIKE A SEALED ENVELOP - only you & server can read it(<!!>)

## MORE EXPLAINATION ON HTTP:

HTTP stands for HYPERTEXT TRANSFER PROTOCOL:= it is the language that browsers and server use to communicate.
EXAMPLE:
1* YOU OPEN A BROWSER
2* YOU TYPE google.com.
3* YOUR BROWSER SENDS AN (HTTP REQUEST)
4* GOOGLE'S SERVER SENDS AND (HTTP RESPONSE)
5* THE BROWSER DISPLAYS THE PAGE.

THINK OF IT LIKE ORDERING FOOD:
you = client(browser)
Restuarant = (server)
order = (request)
food = (respons)

## the 4 magic word (HTTP METHODS)
method ----what it means----------like ordering food
GET      "give me something"    "can i see the menu?
POST     "make something new"   "i want a new pizza"
PUT      "change everything"   "change my whole order
DELETE   "Remove something"     "cancel my pizza"


## important Go package for HTTP

PACKAGE -----------------PURPOSE
net/http                   web servers and client
encoding/json              JSON handing
io                          read request bodies
html/template                HTML templates
context                  Request lifecycle management

1* net/http ==> this is the most important package .
it provides everything needed to:
* create servers
* receive requests
* send responses
* make HTTp requests to other servers

2* io ===> the io package is used for reading and writing data streams.
import "io"
in HTTP, it is commonly used to read the request body .
io.ReadAll() collects everything from thst stream.

3* encoding/json ==> (JSON stands for JavaScript Object Notation) it is a text format used to store and exchange data betweeen applications. JSON is a way of organizing information using key-value pairs:
HERE:
"firstName" is a key
"john" is its values

## why is JSON important?
when a browser, mobile app, or frontend talks to a backend server,they often exchange data as JSON