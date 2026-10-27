import json
import os
import time
from google import genai

File = "tickets.json"

# Terminal Colors
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"
def get_ai_suggestions(description):
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        try:
            client = genai.Client(api_key=api_key, http_options={"timeout": 3.0})
            prompt = (
                "You are an IT support assistant. Analyze the following campus tech support ticket. "
                "You MUST respond ONLY with a valid JSON object containing these exact keys: "
                "'category' (string), 'urgency' (string: Low/Medium/High), and "
                f"'steps' (list of 3-4 concise strings).\n\nTicket: {description}"
            )
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config={"response_mime_type": "application/json"}
            )
            ai_data = json.loads(response.text.strip())
            print(f"\n{GREEN}Cloud AI Analysis Result:{RESET}")
            print(f"Category: {ai_data.get('category')}")
            print(f"Urgency: {ai_data.get('urgency')}")
            return ai_data
        except Exception as e:

            print(f"\n[Debug Cloud Error]: {e}")

    desc_lower = description.lower()
    if "wifi" in desc_lower or "network" in desc_lower or "slow" in desc_lower or "internet" in desc_lower:
        ai_data = {
            "category": "Network & Connectivity",
            "urgency": "High",
            "steps": [
                "Toggle your device's Wi-Fi adapter off and back on.",
                "Forget the campus network and re-enter your credentials.",
                "Verify if other devices can connect to the access point.",
                "Restart your laptop if the network interface is unresponsive."
            ]
        }
    elif "password" in desc_lower or "login" in desc_lower or "account" in desc_lower:
        ai_data = {
            "category": "Authentication",
            "urgency": "Medium",
            "steps": [
                "Clear your browser cache and cookies.",
                "Visit the campus IT portal to use the self-service password reset.",
                "Ensure Caps Lock is disabled.",
                "Contact the helpdesk if your account is locked out."
            ]
        }
    else:
        ai_data = {
            "category": "General Hardware/Software",
            "urgency": "Low",
            "steps": [
                "Restart your device to clear temporary system states.",
                "Check for pending operating system updates.",
                "Describe the error code or symptom in detail for future logs.",
                "Visit the campus IT service desk in person if hardware is damaged."
            ]
        }

    print(f"\n{GREEN}Offline AI Analysis Result (Simulated):{RESET}")
    print(f"Category: {ai_data.get('category')}")
    print(f"Urgency: {ai_data.get('urgency')}")
    print("Suggestions:")
    for i, step in enumerate(ai_data.get('steps', []), 1):
        print(f"  {i}. {step}")

    return ai_data
def create_tickets():
    # Friendly AI welcome prompt
    print(f"\n{CYAN}[CampusFlow AI]: Welcome to CampusFlow problem solving! Tell us your problem and it will get fixed.{RESET}")

    title = input("Enter title: ").strip()
    user_description = input("Enter description: ").strip()

    if not title or not user_description:
        print(f"{YELLOW}Please enter both title and description.{RESET}")
        return

    ticket_id = int(time.time())
    print(f"\n{GREEN}Ticket created successfully.{RESET}")
    print(f"ID: {ticket_id}")
    print(f"Description: {user_description}\n")

    print("Getting AI suggestions...")
    ai_result = get_ai_suggestions(user_description)

    tickets = []
    if os.path.exists(File):
        try:
            with open(File, "r") as file:
                tickets = json.load(file)
        except (json.JSONDecodeError, OSError):
            print(f"{RED}Error: couldn't read JSON file.{RESET}")
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
        print(f"{GREEN}Successfully saved to {File}{RESET}")
    except OSError:
        print(f"{RED}Error: could not save to JSON file.{RESET}")

def view_tickets():
    if not os.path.exists(File):
        print(f"\n{YELLOW}No saved tickets found yet.{RESET}")
        return
    
    try:
        with open(File, "r") as file:
            tickets = json.load(file)

        if not tickets:
            print(f"\n{YELLOW}Your ticket list is empty.{RESET}")
            return
            
        print(f"\n{CYAN}{BOLD}=== Saved Campus Tech Tickets ==={RESET}")
        for ticket in tickets:
            print(f"{BOLD}ID:{RESET} {ticket.get('id', 'N/A')}")
            print(f"{BOLD}Title:{RESET} {ticket.get('title', 'N/A')}")
            print(f"{BOLD}Description:{RESET} {ticket.get('user_description', 'N/A')}")
            
            # Handle structured vs legacy unstructured AI analysis safely
            ai_analysis = ticket.get('ai_analysis', {})
            if isinstance(ai_analysis, dict):
                urgency = ai_analysis.get('urgency', 'Unknown')
                
                # Color code urgency dynamically
                urgency_color = GREEN
                if urgency.lower() == "high":
                    urgency_color = RED
                elif urgency.lower() == "medium":
                    urgency_color = YELLOW

                print(f"{BOLD}Category:{RESET} {ai_analysis.get('category', 'N/A')}")
                print(f"{BOLD}Urgency:{RESET} {urgency_color}{urgency}{RESET}")
                print(f"{BOLD}AI Suggestions:{RESET}")
                for i, step in enumerate(ai_analysis.get('steps', []), 1):
                    print(f"  {i}. {step}")
            else:
                # Fallback for old text-based tickets
                print(f"{BOLD}AI Suggestions:{RESET}\n{ai_analysis}")
                
            print(f"{CYAN}" + "-" * 40 + f"{RESET}")
            
    except (json.JSONDecodeError, OSError):
        print(f"\n{RED}Error: Could not read the tickets file.{RESET}")

def main():
    while True:
        print(f"\n{CYAN}--- CampusFlow IT Support ---{RESET}")
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
            print(f"{YELLOW}Invalid choice. Please enter 1, 2, or 3.{RESET}")

if __name__ == "__main__":
    main()