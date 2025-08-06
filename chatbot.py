from jira_client import fetch_jira_tickets, add_comment_to_ticket
from llm_chain import analyze_ticket
from auto_assign import auto_assign_all, auto_assign_ticket_to_least_loaded, fetch_all_tickets
from config import PROJECT_KEY
from handle_natural_query import handle_natural_query
from concurrent.futures import ThreadPoolExecutor

analyze_cache = {}
executor = ThreadPoolExecutor(max_workers=2)

# Global ticket caches
tickets = []
full_tickets = []

def get_ticket_by_key(tickets, key):
    for ticket in tickets:
        if ticket["key"].lower() == key.lower():
            return ticket
    return None

def refresh_tickets():
    global tickets, full_tickets
    tickets = fetch_jira_tickets()
    full_tickets = fetch_all_tickets()

def analyze_ticket_cached(ticket):
    key = ticket['key']
    if key in analyze_cache:
        return analyze_cache[key]
    future = executor.submit(analyze_ticket, ticket)
    result = future.result()
    analyze_cache[key] = result
    return result

def chatbot():
    print("\U0001F916 Welcome to the Jira AI Chatbot!")
    print("Type 'help' for commands, or 'exit' to quit.\n")

    refresh_tickets()

    while True:
        user_input = input("You > ").strip().lower()

        if user_input in ['exit', 'quit']:
            print("\U0001F44B Goodbye!")
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
- suggest <TICKET_KEY>: RAG-based recommendation using similar past tickets
- auto assign: Automatically assigns unassigned tickets to users with the fewest currently assigned tickets.
- auto assign <TICKET_KEY>: Assign specific ticket using load balancing
- ask <question>: Ask a natural language question (e.g., "Which tickets are unassigned?")
- refresh: Reload ticket data from Jira
""")
            continue

        if user_input == 'refresh':
            refresh_tickets()
            print("\U0001F504 Ticket data refreshed.")
            continue

        if user_input == 'all':
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
                print("\u274C Ticket not found.")
            continue

        elif user_input.startswith('analyze '):
            key = user_input.split(' ')[1]
            ticket = get_ticket_by_key(full_tickets, key)

            if ticket:
                try:
                    result = analyze_ticket_cached(ticket)
                    print("\U0001F9E0 AI Suggestion:\n", result)
                except Exception as e:
                    print(f"\u274C Analysis failed: {e}")
            else:
                print("\u274C Ticket not found.")
            continue

        elif user_input.startswith('comment '):
            key = user_input.split(' ')[1]
            ticket = get_ticket_by_key(full_tickets, key)
            if ticket:
                result = analyze_ticket_cached(ticket)
                add_comment_to_ticket(ticket['key'], result)
                print(f"\u2705 Comment added to {ticket['key']}")
            else:
                print("\u274C Ticket not found.")
            continue

        elif user_input.startswith('suggest '):
            key = user_input.split(' ')[1]
            ticket = get_ticket_by_key(full_tickets, key)
            if ticket:
                try:
                    result = analyze_ticket_cached(ticket)
                    print("\U0001F4CC Suggested Next Steps:\n", result)
                except Exception as e:
                    print(f"\u274C Suggestion failed: {e}")
            else:
                print("\u274C Ticket not found.")
            continue

        elif user_input.startswith("auto assign"):
            parts = user_input.strip().split()
            if len(parts) == 3:
                ticket_key = parts[2].upper()
                print(f"\U0001F504 Assigning {ticket_key} to least-loaded user...")
                try:
                    auto_assign_ticket_to_least_loaded(ticket_key)
                except Exception as e:
                    print(f"\u274C Auto-assign failed: {e}")

            elif len(parts) == 2:
                print("\U0001F504 Running auto assignment for all unassigned tickets...")
                try:
                    auto_assign_all()
                except Exception as e:
                    print(f"\u274C Auto-assign failed: {e}")

            else:
                print("\u274C Usage: auto assign <TICKET_KEY> or auto assign")
            continue

        elif user_input.startswith('ask '):
            query = user_input[4:]
            jql = handle_natural_query(query)
            if jql:
                results = fetch_jira_tickets(jql)
                if results:
                    for t in results:
                        print(f"{t['key']}: {t['summary']}")
                else:
                    print("No matching tickets found.")
            else:
                print("\u274C Sorry, I couldn’t understand that query.")
            continue

        else:
            print("\u2753 Unknown command. Type 'help' for options.")

if __name__ == "__main__":
    chatbot()

