import json
import os
import time

File = "tickets.json"
def create_tickets():
    title = input("Enter title: ").strip()
    user_description = input("Enter description: ").strip()

    if not title or not user_description:
        print("please enter title and description")
        return

        tickets = []
    if os.path.exists(File):
        try:
            with open(File, "r") as file:
                tickets = json.load(file)
        except(json.JSONDecodeError, OSError):
            print("Error: could'nt read to json file")
            tickets = []
        

    tickets.append({
        "id": int(time.time()),
        "title": title,
        "user_description": user_description
    })
    try:
        with open(File, "w") as file:
            json.dump(tickets, file, indent=4)
        print(f"successfuly saved to {File}")
    except OSError:
        print("Error: could not save to JSON file.")
    
create_tickets()

