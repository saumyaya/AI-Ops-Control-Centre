import streamlit as st
from jira_client import fetch_jira_tickets
from auto_assign import auto_assign_all, auto_assign_ticket_to_least_loaded
from handle_natural_query import handle_natural_query

# Helper to flatten Jira API tickets into easy dicts
def flatten_tickets(jira_tickets):
    flat_list = []
    for t in jira_tickets:
        summary = t.get("fields", {}).get("summary", "No summary")
        description = (
            t.get("fields", {})
            .get("description", {})
            .get("content", [{}])[0]
            .get("content", [{}])[0]
            .get("text", "")
        )
        flat_list.append({
            "key": t.get("key", ""),
            "summary": summary,
            "description": description
        })
    return flat_list

st.set_page_config(page_title="Jira AI Chatbot UI", layout="wide")

st.title("🤖 Jira AI Chatbot (UI Version)")
st.write("Manage Jira tickets with AI-powered suggestions, summaries, and automation.")

# Sidebar Navigation
menu = st.sidebar.selectbox(
    "Choose a Command",
    ["All Tickets", "Open Tickets", "Closed Tickets", "Auto Assign All", "Ask Query"]
)

if menu == "All Tickets":
    tickets = flatten_tickets(fetch_jira_tickets())
    if tickets:
        for t in tickets:
            st.write(f"**{t['key']}** — {t['summary']}")
    else:
        st.warning("No tickets found.")

elif menu == "Open Tickets":
    tickets = flatten_tickets(fetch_jira_tickets("statusCategory != Done"))
    if tickets:
        for t in tickets:
            st.write(f"**{t['key']}** — {t['summary']}")
    else:
        st.warning("No open tickets found.")

elif menu == "Closed Tickets":
    tickets = flatten_tickets(fetch_jira_tickets("statusCategory = Done"))
    if tickets:
        for t in tickets:
            st.write(f"**{t['key']}** — {t['summary']}")
    else:
        st.warning("No closed tickets found.")

elif menu == "Auto Assign All":
    if st.button("Run Auto Assignment"):
        auto_assign_all()

elif menu == "Ask Query":
    user_query = st.text_input("Ask a natural language question about tickets:")
    if st.button("Run Query"):
        jql = handle_natural_query(user_query)
        if jql:
            results = flatten_tickets(fetch_jira_tickets(jql))
            if results:
                for t in results:
                    st.write(f"**{t['key']}** — {t['summary']}")
            else:
                st.warning("No matching tickets found.")
        else:
            st.error("❌ Could not understand the query.")

