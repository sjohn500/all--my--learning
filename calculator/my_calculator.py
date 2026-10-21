def add(a, b):
    return a + b

def substract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        return "Division Error: Cannot divide by zero"
        return a / b
   
def main():
    while True:
        print("\n====Calculator Menu====")
        print("1. Addition")
        print("2. Substraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Exit")

        choice = input("Enter choice: (1-5)").strip()
        
        if choice == "5":
            print("Goodbye")
            break
        if choice not in["1", "2", "3", "4"]:
            print("Invalid choice")
            continue

        num1 = input("Enter first value: ").strip()
        num2 = input("Enter second value: ").strip()

        try:
            num1 = float(num1)
            num2 = float(num2)
        except ValueError:
            print("Invalid number: Please enter again")
            continue
        
        if choice == "1":
            result = add(num1, num2)
        elif choice == "2":
            result = substract(num1, num2)
        elif choice == "3":
            result = multiply(num1, num2)
        elif choice == "4":
            result = divide(num1, num2)

        if isinstance(result, str):
            print(result)
        if result.is_integer():
            result = int(result)
            print(result)

if __name__== "__main__":
    main()






        