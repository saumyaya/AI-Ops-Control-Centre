import streamlit as st
from jira_client import fetch_jira_tickets, add_comment_to_ticket
from auto_assign import auto_assign_all, auto_assign_ticket_to_least_loaded, fetch_all_tickets
from handle_natural_query import handle_natural_query

# Lazy import for RAG & LLM to keep startup fast
def analyze_ticket_lazy(ticket):
    from llm_chain import analyze_ticket
    return analyze_ticket(ticket)

def refresh_tickets():
    return fetch_jira_tickets(), fetch_all_tickets()

# --- Streamlit Page Config ---
st.set_page_config(page_title="Jira AI Chatbot", layout="wide")
st.title("🤖 Jira AI Chatbot")
st.caption("A UI version of the CLI chatbot with all commands")

# --- Session State ---
if "tickets" not in st.session_state or "full_tickets" not in st.session_state:
    st.session_state.tickets, st.session_state.full_tickets = refresh_tickets()

# --- Tabs for CLI Command Equivalents ---
tab_all, tab_open, tab_closed, tab_sum, tab_analyze, tab_comment, tab_suggest, tab_assign, tab_ask, tab_refresh = st.tabs([
    "📋 All", "🟢 Open", "🔴 Closed", "📄 Summarize", "🧠 Analyze", "💬 Comment", "📌 Suggest", "🧑‍💼 Auto Assign", "❓ Ask", "🔄 Refresh"
])

# --- All Tickets ---
with tab_all:
    st.subheader("All Tickets")
    st.dataframe(st.session_state.tickets)

# --- Open Tickets ---
with tab_open:
    st.subheader("Open Tickets")
    open_tickets = fetch_jira_tickets("statusCategory != Done")
    st.dataframe(open_tickets)

# --- Closed Tickets ---
with tab_closed:
    st.subheader("Closed Tickets")
    closed_tickets = fetch_jira_tickets("statusCategory = Done")
    st.dataframe(closed_tickets)

# --- Summarize ---
with tab_sum:
    st.subheader("Summarize Ticket")
    ticket_key = st.text_input("Enter Ticket Key (Summarize)")
    if st.button("Summarize"):
        ticket = next((t for t in st.session_state.tickets if t["key"].lower() == ticket_key.lower()), None)
        if ticket:
            st.write(f"**Summary:** {ticket['summary']}")
            st.write(f"**Description:** {ticket['description']}")
        else:
            st.error("Ticket not found.")

# --- Analyze ---
with tab_analyze:
    st.subheader("AI Analyze Ticket")
    ticket_key = st.text_input("Enter Ticket Key (Analyze)")
    if st.button("Analyze"):
        ticket = next((t for t in st.session_state.full_tickets if t["key"].lower() == ticket_key.lower()), None)
        if ticket:
            with st.spinner("Analyzing..."):
                suggestion = analyze_ticket_lazy(ticket)
            st.write("### 🧠 AI Suggestion")
            st.write(suggestion)
        else:
            st.error("Ticket not found.")

# --- Comment ---
with tab_comment:
    st.subheader("Comment on Ticket with AI Suggestion")
    ticket_key = st.text_input("Enter Ticket Key (Comment)")
    if st.button("Comment"):
        ticket = next((t for t in st.session_state.full_tickets if t["key"].lower() == ticket_key.lower()), None)
        if ticket:
            with st.spinner("Generating comment..."):
                suggestion = analyze_ticket_lazy(ticket)
            add_comment_to_ticket(ticket['key'], suggestion)
            st.success(f"✅ Comment added to {ticket['key']}")
        else:
            st.error("Ticket not found.")

# --- Suggest (RAG) ---
with tab_suggest:
    st.subheader("RAG-based Suggestion")
    ticket_key = st.text_input("Enter Ticket Key (Suggest)")
    if st.button("Suggest"):
        ticket = next((t for t in st.session_state.full_tickets if t["key"].lower() == ticket_key.lower()), None)
        if ticket:
            with st.spinner("Retrieving similar tickets and suggesting..."):
                suggestion = analyze_ticket_lazy(ticket)
            st.write("### 📌 Suggested Next Steps")
            st.write(suggestion)
        else:
            st.error("Ticket not found.")

# --- Auto Assign ---
with tab_assign:
    st.subheader("Auto Assign Tickets")
    single_key = st.text_input("Enter Ticket Key (optional)")
    if st.button("Run Auto Assign"):
        if single_key:
            auto_assign_ticket_to_least_loaded(single_key.upper())
            st.success(f"✅ Assigned {single_key.upper()} to least-loaded user")
        else:
            auto_assign_all()
            st.success("✅ Auto-assigned all unassigned tickets")

# --- Ask (Natural Language) ---
with tab_ask:
    st.subheader("Ask Jira in Natural Language")
    query = st.text_input("Ask something like: 'Which tickets are unassigned?'")
    if st.button("Run Query"):
        jql = handle_natural_query(query)
        if jql:
            results = fetch_jira_tickets(jql)
            st.dataframe(results)
        else:
            st.error("Couldn't understand the query.")

# --- Refresh ---
with tab_refresh:
    st.subheader("Refresh Tickets Data")
    if st.button("Refresh Now"):
        st.session_state.tickets, st.session_state.full_tickets = refresh_tickets()
        st.success("🔄 Ticket data refreshed!")
