from jira_client import fetch_jira_tickets, add_comment_to_ticket
from llm_chain import analyze_ticket

def run_ai_ops():
    tickets = fetch_jira_tickets()
    for ticket in tickets:
        key = ticket["key"]
        summary = ticket["summary"]
        description = ticket["description"]

        print(f"🔍 Analyzing {key}: {summary}")
        
        ai_response = analyze_ticket({
            "key": key,
            "summary": summary,
            "description": description
        })

        print("🧠 AI Suggestion:\n", ai_response)

        add_comment_to_ticket(key, ai_response)

if __name__ == "__main__":
    run_ai_ops()

