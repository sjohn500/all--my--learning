try:
    print("Line 1: Runs fine.")
    result = 10 / 0
    print("Line 3: Skipped!")
except ZeroDivisionError:
    print("Line 4: Caught the error")

############################

try:
    result = 10 / 2
    print("Line A")
    result_2 = 5 / 0
    print("Line B")
except ZeroDivisionError:
    print("Line C")


#######################################
try:
    user_input = input("Enter a number: ")
    number = int(user_input)
    result = 100/ number
    print(f"Result is {result}")
except ValuesError:
    print("Error: You must type a valid number!")
except ZoreDivisionError:
    print("Error: You cannot divide by zero!")
##############################################

try:
    user_age = int(input("Enter your age: "))
    days_alive = 365 / user_age
    print(f"Calculation complete: {days_alive}")
except ValueError:
    print("Error Code: Orange")
except ZeroDivisionError:
    print("Error Code: Purple")
