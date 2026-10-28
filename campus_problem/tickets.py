import os
import json
import time
import random
import requests

# --- ANSI Color Codes ---
RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
GRAY = "\033[90m"

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
    
    max_retries = 2
    for attempt in range(max_retries):
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=20.0)
            if response.status_code == 200:
                content = response.json()["candidates"][0]["content"]["parts"][0]["text"]
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0].strip()
                elif "```" in content:
                    content = content.split("```")[1].split("```")[0].strip()
                return json.loads(content)
            elif response.status_code == 503 and attempt < max_retries - 1:
                time.sleep(1.5)
                continue
            else:
                raise Exception(f"Gemini returned status code {response.status_code}: {response.text}")
        except requests.exceptions.Timeout:
            if attempt < max_retries - 1:
                time.sleep(1.0)
                continue
            raise Exception("Gemini request timed out after retries.")
            
    raise Exception("Gemini failed after maximum retry attempts.")

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
        print(f"\n{MAGENTA}[AI] Using Gemini...{RESET}")
        try:
            return analyze_with_gemini(description)
        except Exception as e:
            print(f"{RED}[Error] Gemini failed: {e}. Falling back to Heuristic Engine.{RESET}")
            return heuristic_analysis(description)
            
    elif choice == '2':
        print(f"\n{MAGENTA}[AI] Using OpenRouter...{RESET}")
        try:
            return analyze_with_openrouter(description)
        except Exception as e:
            print(f"{RED}[Error] OpenRouter failed: {e}. Falling back to Heuristic Engine.{RESET}")
            return heuristic_analysis(description)
            
    else:  # Auto-Cascade
        print(f"\n{MAGENTA}[AI] Using Auto-Cascade...{RESET}")
        try:
            print(f"{GRAY}[Cascade] Attempting Gemini...{RESET}")
            return analyze_with_gemini(description)
        except Exception as e1:
            print(f"{YELLOW}[Cascade] Gemini skipped/failed: {e1}{RESET}")
            try:
                print(f"{GRAY}[Cascade] Attempting OpenRouter...{RESET}")
                return analyze_with_openrouter(description)
            except Exception as e2:
                print(f"{RED}[Cascade] OpenRouter skipped/failed: {e2}. Falling back to Heuristic Engine.{RESET}")
                return heuristic_analysis(description)

def create_ticket():
    title = input(f"{CYAN}Enter title: {RESET}")
    description = input(f"{CYAN}Enter description: {RESET}")
    
    print(f"\n{BOLD}Select AI Engine:{RESET}")
    print("1. Gemini")
    print("2. OpenRouter")
    print("3. Auto-Cascade (Default)")
    choice = input(f"{CYAN}Choose AI provider (1-3): {RESET}").strip()
    if choice not in ['1', '2', '3']:
        choice = '3'
        
    ticket_id = random.randint(1000000000, 9999999999)
    print(f"\n{GREEN}✔ Ticket created successfully.{RESET}")
    print(f"{BOLD}ID:{RESET} {ticket_id}")
    print(f"{BOLD}Description:{RESET} {description}")
    
    print(f"\n{BLUE}Getting AI suggestions...{RESET}")
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
    
    print(f"\n{CYAN}{BOLD}Suggestions:{RESET}")
    for i, step in enumerate(analysis.get("steps", []), 1):
        print(f"{GREEN}{i}.{RESET} {step}")

def view_tickets():
    tickets = load_tickets()
    if not tickets:
        print(f"\n{YELLOW}No saved tickets found.{RESET}")
        return
    print(f"\n{CYAN}{BOLD}--- Saved Tickets ---{RESET}")
    for t in tickets:
        urgency = t['urgency']
        if urgency == "High":
            urgency_str = f"{RED}{urgency}{RESET}"
        elif urgency == "Medium":
            urgency_str = f"{YELLOW}{urgency}{RESET}"
        else:
            urgency_str = f"{GREEN}{urgency}{RESET}"
            
        print(f"{BOLD}ID:{RESET} {t['id']} | {BOLD}Title:{RESET} {t['title']} | {BOLD}Category:{RESET} {t['category']} | {BOLD}Urgency:{RESET} {urgency_str}")
        print(f"{GRAY}Description: {t['description']}{RESET}")
        print(f"{BOLD}Steps:{RESET}")
        for i, s in enumerate(t['steps'], 1):
            print(f"  {i}. {s}")
        print(f"{GRAY}{'-' * 30}{RESET}")

def show_help():
    print(f"\n{CYAN}{BOLD}=== CampusFlow System & Help Guide ==={RESET}")
    print(f"{BOLD}Description:{RESET} CampusFlow is a high-resilience IT support CLI tool designed")
    print("to categorize issues, assess urgency, and generate troubleshooting steps.")
    
    print(f"\n{BOLD}1. Architecture & Auto-Cascade:{RESET}")
    print(f"   • {GREEN}Tier 1 (Gemini):{RESET} Primary intelligence engine with 20s timeout & auto-retry.")
    print(f"   • {YELLOW}Tier 2 (OpenRouter):{RESET} Secondary fallback cloud model.")
    print(f"   • {RED}Tier 3 (Heuristic Local Engine):{RESET} Offline fallback ruleset ensuring zero downtime.")
    
    print(f"\n{BOLD}2. Environment Variables Required:{RESET}")
    print(f"   • {CYAN}GEMINI_API_KEY{RESET} (or GOOGLE_API_KEY)")
    print(f"   • {CYAN}OPENROUTER_API_KEY{RESET}")
    
    print(f"\n{BOLD}3. Terminal Color Guide:{RESET} ")
    print(f"   • {GREEN}Green:{RESET} Success states & low urgency / step indices")
    print(f"   • {YELLOW}Yellow:{RESET} Medium urgency & fallback warnings")
    print(f"   • {RED}Red:{RESET} High urgency & connection error alerts")
    print(f"   • {CYAN}Cyan:{RESET} Headers, titles, and user prompt inputs")
    print(f"{CYAN}{'-' * 45}{RESET}")

def main():
    while True:
        print(f"\n{CYAN}{BOLD}=== CampusFlow IT Support ==={RESET}")
        print("1. Create a new ticket")
        print("2. View saved tickets")
        print("3. System & Help Guide")
        print("4. Exit")
        choice = input(f"{CYAN}Choose an option (1-4): {RESET}").strip()
        
        if choice == '1':
            create_ticket()
        elif choice == '2':
            view_tickets()
        elif choice == '3':
            show_help()
        elif choice == '4':
            print(f"\n{GREEN}Goodbye!{RESET}\n")
            break
        else:
            print(f"{RED}Invalid option. Please choose between 1 and 4.{RESET}")

if __name__ == "__main__":
    main()