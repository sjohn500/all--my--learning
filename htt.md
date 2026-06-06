## what is HTTP?

the full meaning of HTTP is HYPERTEXT TRANSFER PROTOCOL

EXPLAINATION :
let me build you a vilsual story:
you(BROWSER):Sitting at the table hungry for a webpage
(HTTP): the waiter that carries your order & food 
server(KICHEN): stores & prepares the wabpage for you

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