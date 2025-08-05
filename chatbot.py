from jira_client import fetch_jira_tickets, add_comment_to_ticket
from llm_chain import analyze_ticket

def get_ticket_by_key(tickets, key):
    for ticket in tickets:
        if ticket["key"].lower() == key.lower():
            return ticket
    return None

def chatbot():
    print("🤖 Welcome to the Jira AI Chatbot!")
    print("Type 'help' for commands, or 'exit' to quit.\n")

    tickets = fetch_jira_tickets()

    while True:
        user_input = input("You > ").strip().lower()

        if user_input in ['exit', 'quit']:
            print("👋 Goodbye!")
            break

        if user_input == 'help':
            print("""
Commands:
- all: Show all tickets
- open: Show open tickets
- closed: Show closed tickets
- summarize <TICKET_KEY>: Show summary and description
- analyze <TICKET_KEY>: Run AI analysis
- comment <TICKET_KEY>: Run AI analysis and comment on Jira
""")
            continue

        if user_input == 'all':
            tickets = fetch_jira_tickets()
            for t in tickets:
                print(f"{t['key']}: {t['summary']}")
            continue

        if user_input == 'open':
            open_tickets = fetch_jira_tickets("statusCategory != Done")
            for t in open_tickets:
                print(f"{t['key']}: {t['summary']}")
            continue

        if user_input == 'closed':
            closed_tickets = fetch_jira_tickets("statusCategory = Done")
            for t in closed_tickets:
                print(f"{t['key']}: {t['summary']}")
            continue

        if user_input.startswith('summarize '):
            key = user_input.split(' ')[1]
            ticket = get_ticket_by_key(tickets, key)
            if ticket:
                print(f"Summary: {ticket['summary']}")
                print(f"Description: {ticket['description']}")
            else:
                print("❌ Ticket not found.")
            continue

        if user_input.startswith('analyze '):
            key = user_input.split(' ')[1]
            ticket = get_ticket_by_key(tickets, key)
            if ticket:
                result = analyze_ticket(ticket)
                print("🧠 AI Suggestion:\n", result)
            else:
                print("❌ Ticket not found.")
            continue

        if user_input.startswith('comment '):
            key = user_input.split(' ')[1]
            ticket = get_ticket_by_key(tickets, key)
            if ticket:
                result = analyze_ticket(ticket)
                add_comment_to_ticket(ticket['key'], result)
                print(f"✅ Comment added to {ticket['key']}")
            else:
                print("❌ Ticket not found.")
            continue

        print("❓ Unknown command. Type 'help' for options.")

if __name__ == "__main__":
    chatbot()

