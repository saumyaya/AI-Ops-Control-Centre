from jira_client import fetch_jira_tickets, add_comment_to_ticket
from llm_chain import analyze_ticket
from auto_assign import auto_assign_all, auto_assign_ticket_to_least_loaded
from config import PROJECT_KEY

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
- auto assign: Automatically assigns unassigned tickets to users with the fewest currently assigned tickets.
""")
            continue

        if user_input == 'all':
            tickets = fetch_jira_tickets()
            for t in tickets:
                print(f"{t['key']}: {t['summary']}")
            continue

        elif user_input == 'open':
            open_tickets = fetch_jira_tickets("statusCategory != Done")
            for t in open_tickets:
                print(f"{t['key']}: {t['summary']}")
            continue

        elif user_input == 'closed':
            closed_tickets = fetch_jira_tickets("statusCategory = Done")
            for t in closed_tickets:
                print(f"{t['key']}: {t['summary']}")
            continue

        elif user_input.startswith('summarize '):
            key = user_input.split(' ')[1]
            ticket = get_ticket_by_key(tickets, key)
            if ticket:
                print(f"Summary: {ticket['summary']}")
                print(f"Description: {ticket['description']}")
            else:
                print("❌ Ticket not found.")
            continue

        elif user_input.startswith('analyze '):
            key = user_input.split(' ')[1]
            ticket = get_ticket_by_key(tickets, key)
            if ticket:
                result = analyze_ticket(ticket)
                print("🧠 AI Suggestion:\n", result)
            else:
                print("❌ Ticket not found.")
            continue

        elif user_input.startswith('comment '):
            key = user_input.split(' ')[1]
            ticket = get_ticket_by_key(tickets, key)
            if ticket:
                result = analyze_ticket(ticket)
                add_comment_to_ticket(ticket['key'], result)
                print(f"✅ Comment added to {ticket['key']}")
            else:
                print("❌ Ticket not found.")
            continue

        elif user_input.startswith("auto assign"):
            parts = user_input.strip().split()
            if len(parts) == 3:
            # Command: auto assign <TICKET_KEY>
                ticket_key = parts[2].upper()
                print(f"🔄 Assigning {ticket_key} to least-loaded user...")
                try:
                    auto_assign_ticket_to_least_loaded(ticket_key)
                except Exception as e:
                    print(f"❌ Auto-assign failed: {e}")

            elif len(parts) == 2:
            # Command: auto assign (all unassigned)
                print("🔄 Running auto assignment for all unassigned tickets...")
                try:
                    auto_assign_all()
                except Exception as e:
                    print(f"❌ Auto-assign failed: {e}")

            else:
                print("❌ Usage: auto assign <TICKET_KEY> or auto assign")

            continue
        else:
            print("❓ Unknown command. Type 'help' for options.")

if __name__ == "__main__":
    chatbot()

