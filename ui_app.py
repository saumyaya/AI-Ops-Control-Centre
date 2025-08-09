import streamlit as st
from jira_client import fetch_jira_tickets, add_comment_to_ticket
from auto_assign import auto_assign_all, auto_assign_ticket_to_least_loaded
from handle_natural_query import handle_natural_query

# Lazy import for RAG & LLM to keep startup fast
def analyze_ticket_lazy(ticket):
    from llm_chain import analyze_ticket
    return analyze_ticket(ticket)

st.set_page_config(page_title="Jira AI Chatbot", layout="wide")
st.title("🤖 Jira AI Chatbot (Web UI)")

# Sidebar commands
command = st.sidebar.selectbox(
    "Select Command",
    [
        "All Tickets",
        "Open Tickets",
        "Closed Tickets",
        "Summarize Ticket",
        "Analyze Ticket",
        "Comment on Ticket",
        "Suggest Next Steps",
        "Auto Assign All",
        "Auto Assign One",
        "Ask Natural Query"
    ]
)

# Show all tickets
if command == "All Tickets":
    tickets = fetch_jira_tickets()
    for t in tickets:
        st.write(f"{t['key']}: {t['summary']}")

elif command == "Open Tickets":
    tickets = fetch_jira_tickets("statusCategory != Done")
    for t in tickets:
        st.write(f"{t['key']}: {t['summary']}")

elif command == "Closed Tickets":
    tickets = fetch_jira_tickets("statusCategory = Done")
    for t in tickets:
        st.write(f"{t['key']}: {t['summary']}")

elif command == "Summarize Ticket":
    key = st.text_input("Enter Ticket Key")
    if st.button("Summarize"):
        tickets = fetch_jira_tickets(f"key = {key}")
        if tickets:
            ticket = tickets[0]
            st.write(f"Summary: {ticket['summary']}")
            st.write(f"Description: {ticket['description']}")
        else:
            st.error("Ticket not found.")

elif command == "Analyze Ticket":
    key = st.text_input("Enter Ticket Key")
    if st.button("Analyze"):
        tickets = fetch_jira_tickets(f"key = {key}")
        if tickets:
            ticket = tickets[0]
            try:
                result = analyze_ticket_lazy(ticket)
                st.success("AI Suggestion:")
                st.write(result)
            except Exception as e:
                st.error(f"Analysis failed: {e}")
        else:
            st.error("Ticket not found.")

elif command == "Comment on Ticket":
    key = st.text_input("Enter Ticket Key")
    if st.button("Analyze & Comment"):
        tickets = fetch_jira_tickets(f"key = {key}")
        if tickets:
            ticket = tickets[0]
            result = analyze_ticket_lazy(ticket)
            add_comment_to_ticket(ticket['key'], result)
            st.success(f"Comment added to {ticket['key']}")
        else:
            st.error("Ticket not found.")

elif command == "Suggest Next Steps":
    key = st.text_input("Enter Ticket Key")
    if st.button("Suggest"):
        tickets = fetch_jira_tickets(f"key = {key}")
        if tickets:
            ticket = tickets[0]
            try:
                result = analyze_ticket_lazy(ticket)
                st.info("Suggested Next Steps:")
                st.write(result)
            except Exception as e:
                st.error(f"Suggestion failed: {e}")
        else:
            st.error("Ticket not found.")

elif command == "Auto Assign All":
    if st.button("Run Auto Assign"):
        auto_assign_all()

elif command == "Auto Assign One":
    key = st.text_input("Enter Ticket Key")
    if st.button("Assign"):
        auto_assign_ticket_to_least_loaded(key)
        st.success(f"{key} assigned to least-loaded user.")

elif command == "Ask Natural Query":
    query = st.text_input("Ask a question (e.g., 'Which tickets are unassigned?')")
    if st.button("Search"):
        jql = handle_natural_query(query)
        if jql:
            results = fetch_jira_tickets(jql)
            if results:
                for t in results:
                    st.write(f"{t['key']}: {t['summary']}")
            else:
                st.warning("No matching tickets found.")
        else:
            st.error("Could not understand query.")
