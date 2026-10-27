import json
import os
import time
from google import genai

File = "tickets.json"

def get_ai_suggestions(description):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("\n[Error] GEMINI_API_KEY environment variable is missing.")
        print("please set it in your terminal using: export GEMINI_API_KEY='your_key")
        return "AI analyisi skipped (missing API key)"
    try:
        client = genai.Client(
            api_key=api_key,
            http_options={"timeout": 5.0}
        )

        prompt = (
            "You are an IT support assistant. Analyze the following campus tech support ticket "
            f"and provide 3-4 concise, numbered troubleshooting steps:\n\n{description}"
        )
        

        response = client.models.generate_content(
            model ='gemini-3.8-flash',
            contents=prompt
        )

        suggestions = response.text.strip()
        print("\nSuggestions:")
        print(suggestions)
        
        return suggestions
    except Exception as e:
        if "503" in str(e) or "UNAVAILABLE" in str(e):
            print("\n[AI Notice] Google's servers are busy right now. Saving ticket without AI analysis.")
            return "AI analysis pending (Timout/Server busy)"
        
        print(f"\n[Error] Failed to get AI suggestions: {e}")
        return "AI analysis failed due to a system error."

def create_tickets():
    title = input("Enter title: ").strip()
    user_description = input("Enter description: ").strip()

    if not title or not user_description:
        print("please enter title and description")
        return


    ticket_id = int(time.time())
    print("\nTicket created successfully.")
    print(f"ID: {ticket_id}")
    print(f"Description: {user_description}\n")

    print("Getting AI suggestions...")
    ai_result = get_ai_suggestions(user_description)


    tickets = []

    if os.path.exists(File):
        try:
            with open(File, "r") as file:
                tickets = json.load(file)
        except(json.JSONDecodeError, OSError):
            print("Error: could'nt read to json file")
            tickets = []


    tickets.append({
        "id": ticket_id,
        "title": title,
        "user_description": user_description,
        "ai_analysis": ai_result
    })

   
    try:
        with open(File, "w") as file:
            json.dump(tickets, file, indent=4)
        print(f"successfuly saved to {File}")
    except OSError:
        print("Error: could not save to JSON file.")
  
def view_tickets():
    if not os.path.exists(File):
        print("\nNo saved tickets found yet.")
        return
    
    try:
        with open(File, "r") as file:
            tickets = json.load(file)

        if not tickets:
            print("\nYour ticket list is empty.")
            return
            
        print("\n=== Saved Campus Tech Tickets ===")
        for ticket in tickets:
            print(f"ID: {ticket.get('id', 'N/A')}")
            print(f"Title: {ticket.get('title', 'N/A')}")
            print(f"Description: {ticket.get('user_description', 'N/A')}")
            # Use .get() so it doesn't crash if a key is missing!
            print(f"AI Suggestions:\n{ticket.get('ai_analysis', 'No analysis available')}")
            print("-" * 40)
            
    except (json.JSONDecodeError, OSError):
        print("\nError: Could not read the tickets file.")
def main():
    while True:
        print("\n--- CampusFlow IT Support ---")
        print("1. Create a new ticket")
        print("2. View saved tickets")
        print("3. Exit")
        
        choice = input("Choose an option (1-3): ").strip()
        
        if choice == "1":
            create_tickets()
        elif choice == "2":
            view_tickets()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()


 