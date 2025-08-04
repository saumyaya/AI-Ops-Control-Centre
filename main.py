from jira_client import fetch_jira_tickets, post_comment
from llm_chain import analyze_ticket

def run_ai_ops():
    tickets = fetch_jira_tickets()
    for ticket in tickets:
        print(f"🔍 Analyzing {ticket['key']}: {ticket['summary']}")
        response = analyze_ticket(ticket)
        print(response)
        post_comment(ticket['key'], response)

if __name__ == "__main__":
    run_ai_ops()
