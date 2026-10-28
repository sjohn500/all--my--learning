import os
import json
import random
import requests

TICKET_FILE = "tickets.json"

def load_tickets():
    if not os.path.exists(TICKET_FILE):
        return []
    with open(TICKET_FILE, "r") as f:
        return json.load(f)

def save_tickets(tickets):
    with open(TICKET_FILE, "w") as f:
        json.dump(tickets, f, indent=4)

def heuristic_analysis(description):
    desc = description.lower()
    if "wifi" in desc or "network" in desc or "internet" in desc:
        return {
            "category": "Network",
            "urgency": "Medium",
            "steps": [
                "Check whether other devices can access the internet.",
                "Disconnect and reconnect to the Wi-Fi network.",
                "Verify the network gateway and DNS configuration.",
                "Restart the network connection."
            ]
        }
    elif "password" in desc or "login" in desc or "account" in desc:
        return {
            "category": "Authentication",
            "urgency": "High",
            "steps": [
                "Clear browser cache and cookies.",
                "Verify your campus credentials on the main portal.",
                "Use the self-service password reset utility.",
                "Contact the IT helpdesk if account is locked."
            ]
        }
    else:
        return {
            "category": "General Hardware/Software",
            "urgency": "Low",
            "steps": [
                "Restart your device to clear temporary system states.",
                "Check for pending operating system updates.",
                "Describe the error code or symptom in detail.",
                "Visit the campus IT service desk if issues persist."
            ]
        }

def analyze_with_gemini(description):
    gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not gemini_key:
        raise Exception("GEMINI_API_KEY not set.")
    gemini_key = gemini_key.strip()
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key={gemini_key}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{
            "parts": [{
                "text": f"Return ONLY a valid JSON object with keys: 'category' (string), 'urgency' (Low/Medium/High), and 'steps' (list of 4 concise troubleshooting strings). Ticket description: {description}"
            }]
        }]
    }
    response = requests.post(url, headers=headers, json=payload, timeout=20.0)
    if response.status_code == 200:
        content = response.json()["candidates"][0]["content"]["parts"][0]["text"]
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        return json.loads(content)
    raise Exception(f"Gemini returned status code {response.status_code}: {response.text}")

def analyze_with_openrouter(description):
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    if not openrouter_key:
        raise Exception("OPENROUTER_API_KEY not set.")
    openrouter_key = openrouter_key.strip()
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {openrouter_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "openrouter/free",
        "messages": [
            {"role": "system", "content": "Return ONLY a valid JSON object with keys: 'category' (string), 'urgency' (Low/Medium/High), and 'steps' (list of 4 concise troubleshooting strings)."},
            {"role": "user", "content": f"Ticket description: {description}"}
        ]
    }
    response = requests.post(url, headers=headers, json=payload, timeout=20.0)
    if response.status_code == 200:
        content = response.json()["choices"][0]["message"]["content"]
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        return json.loads(content)
    raise Exception(f"OpenRouter returned status code {response.status_code}: {response.text}")

def analyze_ticket(description, choice):
    if choice == '1':
        print("\n[AI] Using Gemini...")
        try:
            return analyze_with_gemini(description)
        except Exception as e:
            print(f"[Error] Gemini failed: {e}. Falling back to Heuristic Engine.")
            return heuristic_analysis(description)
            
    elif choice == '2':
        print("\n[AI] Using OpenRouter...")
        try:
            return analyze_with_openrouter(description)
        except Exception as e:
            print(f"[Error] OpenRouter failed: {e}. Falling back to Heuristic Engine.")
            return heuristic_analysis(description)
            
    else:  # Auto-Cascade
        print("\n[AI] Using Auto-Cascade...")
        try:
            print("[Cascade] Attempting Gemini...")
            return analyze_with_gemini(description)
        except Exception as e1:
            print(f"[Cascade] Gemini skipped/failed: {e1}")
            try:
                print("[Cascade] Attempting OpenRouter...")
                return analyze_with_openrouter(description)
            except Exception as e2:
                print(f"[Cascade] OpenRouter skipped/failed: {e2}. Falling back to Heuristic Engine.")
                return heuristic_analysis(description)

def create_ticket():
    title = input("Enter title: ")
    description = input("Enter description: ")
    
    print("\nSelect AI Engine:")
    print("1. Gemini")
    print("2. OpenRouter")
    print("3. Auto-Cascade (Default)")
    choice = input("Choose AI provider (1-3): ").strip()
    if choice not in ['1', '2', '3']:
        choice = '3'
        
    ticket_id = random.randint(1000000000, 9999999999)
    print(f"\nTicket created successfully.")
    print(f"ID: {ticket_id}")
    print(f"Description: {description}")
    
    print("\nGetting AI suggestions...")
    analysis = analyze_ticket(description, choice)
    
    ticket_data = {
        "id": ticket_id,
        "title": title,
        "description": description,
        "category": analysis.get("category", "General"),
        "urgency": analysis.get("urgency", "Low"),
        "steps": analysis.get("steps", [])
    }
    
    tickets = load_tickets()
    tickets.append(ticket_data)
    save_tickets(tickets)
    
    print(f"\nSuggestions:")
    for i, step in enumerate(analysis.get("steps", []), 1):
        print(f"{i}. {step}")

def view_tickets():
    tickets = load_tickets()
    if not tickets:
        print("\nNo saved tickets found.")
        return
    print("\n--- Saved Tickets ---")
    for t in tickets:
        print(f"ID: {t['id']} | Title: {t['title']} | Category: {t['category']} | Urgency: {t['urgency']}")
        print(f"Description: {t['description']}")
        print("Steps:")
        for i, s in enumerate(t['steps'], 1):
            print(f"  {i}. {s}")
        print("-" * 25)

def main():
    while True:
        print("\n--- CampusFlow IT Support ---")
        print("1. Create a new ticket")
        print("2. View saved tickets")
        print("3. Exit")
        choice = input("Choose an option (1-3): ").strip()
        
        if choice == '1':
            create_ticket()
        elif choice == '2':
            view_tickets()
        elif choice == '3':
            print("\nGoodbye!")
            break
        else:
            print("Invalid option. Please choose 1, 2, or 3.")

if __name__ == "__main__":
    main()