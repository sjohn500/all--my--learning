
resources = [
  {"id": "R001", "name": "Laptop", "category": "Electronics", "total": 10, "available": 10},
  {"id": "R002", "name": "Keyboard", "category": "Accessories", "total": 5, "available": 5},
  {"id": "R003", "name": "Headset", "category": "Accessories", "total": 3, "available": 3}
]
fellows = {"F001": "Ada", "F002": "John", "F003": "Grace"}
borrow_records = []

General_res = {}
for item in resources:
    General_res = item
    print(General_res)

def add_resource_system():
    print("\n--> WELCOME TO RESOURCE SYSTEM ===")
    new_id = input("Enter new ID: ").strip().upper()
    new_name = input("Enter new id name: ")
    print(f"Success: {new_name} added into inventory.")

def add_borrow_system():
    print("\n--> WELCOME TO BORROW SYSTEM===")
    fellows_id = input("Enter Fellow ID: ").strip().upper()
    resources_id = input("Enter Resource ID: ").strip().upper()
    amount = int(input("Enter amount: "))
    if fellows_id not in fellows:
        print("Rejected ID")
        return
        
    for item in resources:
        if amount <= item["available"] and amount > 0:
           item["available"] = item["available"] - amount
           borrow_records.append({"fellows_id": fellows_id, "resource_id": resources_id, "quantity": amount})
           print(f"Accepted: {fellows_id} log successful")
           print(f"Updated Stock: {item["name"]} now has {item['available']} left.")
           print("amount found in resources")
        elif amount <= 0:
            print("amount can not be negative or 0")
        else:
            print("Rejected: Resources ID not found")

def return_resources_system():
    print("\n---> WELCOME TO RETRUN RESOURCE SYSTEM===")
    f_id = input("Enter Fellow ID: ").stip().upper()
    r_id = input("Enter resource ID: ").stip().upper()
    print("proceesing your transaction")

def search_inventory_system():
    print("\n---WELCOME TO SEARCH INVENTORY SYSTEM===")
    query = input("Enter item name to search: ").strip()
    if query  in fellows:
        print("Found item name in resources")

    else:
        print("Item not found in resources")
    
def generate_report_system():
    print("--> WELCOME TO GENERATE REPORT SYSTEM===")
    print("Report completed")


while True:
    print("\n=========================")
    print("======MANAGEMENT SYSTEM========\n")
    print ("1. Add Resource System")
    print("2. Borrow Resource System")
    print("3. Return Resource System")
    print("4. Search / Filter System")
    print("5. View Report Summary System")
    print("6. Exit Application")
    user_choice = input("Enter choice (1-6): ")
 
    if user_choice == "1":
        add_resource_system()
    if user_choice == "2":
        add_borrow_system()
    if user_choice == "3":
        return_resources_system()
    if user_choice == "4":
        search_inventory_system()
    if user_choice =="5":
        generate_report_system()
    if user_choice == "6":
        print("\nShutting down all system safely. Goodbye")
        break

