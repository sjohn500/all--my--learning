import os
import json
import time
import socket
from google import genai

# --- IPv4 Socket Patch (Bypasses [Errno 101] network unreachable) ---
try:
    old_getaddrinfo = socket.getaddrinfo
    def new_getaddrinfo(*args, **kwargs):
        responses = old_getaddrinfo(*args, **kwargs)
        return [r for r in responses if r[0] == socket.AF_INET]
    socket.getaddrinfo = new_getaddrinfo
except Exception:
    pass

TICKETS_FILE = "tickets.json"

def load_tickets():
    """Load existing tickets from JSON file."""
    if os.path.exists(TICKETS_FILE):
        try:
            with open(TICKETS_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []

def save_ticket(ticket):
    """Save a new ticket to the JSON file."""
    tickets = load_tickets()
    tickets.append(ticket)
    with open(TICKETS_FILE, "w") as f:
        json.dump(tickets, f, indent=4)

def update_ticket_in_file(updated_ticket):
    """Update an existing ticket with AI analysis results."""
    tickets = load_tickets()
    for i, t in enumerate(tickets):
        if t["id"] == updated_ticket["id"]:
            tickets[i] = updated_ticket
            break
    with open(TICKETS_FILE, "w") as f:
        json.dump(tickets, f, indent=4)

def get_ai_suggestions(description):
    """Send description to AI model with offline fallback."""
    api_key = os.getenv("GEMINI_API_KEY")
    
    # Try Live Cloud AI Model
    if api_key:
        try:
            client = genai.Client(api_key=api_key)
            prompt = (
                "You are an expert IT support assistant. Analyze the following campus support ticket. "
                "You MUST respond ONLY with a valid JSON object containing these exact keys: "
                "'category' (string), 'urgency' (string: Low/Medium/High), and "
                f"'steps' (list of 4 concise troubleshooting strings).\n\nTicket: {description}"
            )
            
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config={"response_mime_type": "application/json"}
            )
            
            ai_data = json.loads(response.text.strip())
            print(f"\nSuggestions:")
            for i, step in enumerate(ai_data.get('steps', []), 1):
                print(f"{i}. {step}")
            return ai_data
            
        except Exception:
            pass # Fall back silently to heuristic engine

    # Offline Heuristic Engine Fallback
    desc_lower = description.lower()
    if "wifi" in desc_lower or "network" in desc_lower or "slow" in desc_lower or "internet" in desc_lower:
        ai_data = {
            "category": "Network & Connectivity",
            "urgency": "High",
            "steps": [
                "Check whether other devices can access the internet.",
                "Disconnect and reconnect to the Wi-Fi network.",
                "Verify the network gateway and DNS configuration.",
                "Restart the network connection."
            ]
        }
    else:
        ai_data = {
            "category": "General Hardware/Software",
            "urgency": "Low",
            "steps": [
                "Restart your device to clear temporary system states.",
                "Check for pending operating system updates.",
                "Describe the error code or symptom in detail.",
                "Visit the campus IT service desk if issues persist."
            ]
        }

    print(f"\nSuggestions:")
    for i, step in enumerate(ai_data.get('steps', []), 1):
        print(f"{i}. {step}")

    return ai_data

def main():
    while True:
        print("\n--- CampusFlow IT Support ---")
        print("1. Create a new ticket")
        print("2. View saved tickets")
        print("3. Exit")
        
        choice = input("Choose an option (1-3): ").strip()
        
        if choice == "1":
            title = input("Enter title: ").strip()
            description = input("Enter description: ").strip()
            
            # Step 1: Create Ticket ID
            ticket_id = str(int(time.time()))
            
            # Step 2: Prepare and Save Ticket to tickets.json immediately
            new_ticket = {
                "id": ticket_id,
                "title": title,
                "description": description,
                "category": "Unanalyzed",
                "urgency": "Normal",
                "steps": []
            }
            save_ticket(new_ticket)
            
            # Display creation success & details
            print(f"\nTicket created successfully.")
            print(f"\nID: {ticket_id}")
            print(f"Description: {description}")
            
            # Step 3 & 4: Send Ticket Description to AI & Analyze
            print(f"\nGetting AI suggestions...")
            ai_results = get_ai_suggestions(description)
            
            # Update saved ticket with AI analysis results
            new_ticket["category"] = ai_results.get("category", "General")
            new_ticket["urgency"] = ai_results.get("urgency", "Normal")
            new_ticket["steps"] = ai_results.get("steps", [])
            update_ticket_in_file(new_ticket)
            
        elif choice == "2":
            tickets = load_tickets()
            if not tickets:
                print("\nNo saved tickets found.")
            else:
                print(f"\n--- Saved Tickets ({len(tickets)}) ---")
                for t in tickets:
                    print(f"ID: {t['id']} | Title: {t['title']} | Category: {t['category']}")
                    print(f"Description: {t['description']}")
                    print("Suggestions:")
                    for i, step in enumerate(t['steps'], 1):
                        print(f"{i}. {step}")
                    print("-" * 30)
                    
        elif choice == "3":
            print("\nGoodbye!")
            break
        else:
            print("\nInvalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()