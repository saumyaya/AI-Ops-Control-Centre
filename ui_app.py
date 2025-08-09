import streamlit as st
from jira_client import fetch_jira_tickets, add_comment_to_ticket
from auto_assign import auto_assign_all, auto_assign_ticket_to_least_loaded
from handle_natural_query import handle_natural_query

# Lazy load RAG + LLM
def analyze_ticket_lazy(ticket):
    from llm_chain import analyze_ticket
    return analyze_ticket(ticket)

# Helper to flatten Jira API tickets
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
            "description": description,
            "raw": t
        })
    return flat_list

st.set_page_config(page_title="Jira AI Chatbot UI", layout="wide")
st.title("🤖 Jira AI Chatbot (UI Version)")
menu = st.sidebar.selectbox(
    "Choose a Command",
    [ "All Tickets",
        "Open Ticets",
        "Closed Tickets",
        "Summarize Ticket",
        "AI Analysis",
        "Comment",
        "Suggest Solution",
        "Auto Assign",
        "Ask",
        "Refresh"]
)


if menu == "All Tickets":
    tickets = flatten_tickets(fetch_jira_tickets())
    for t in tickets:
        st.subheader(t['key'])  
        st.write(f"**Summary:** {t['summary']}")
        st.write(f"**Description:** {t['description']}")


elif menu == "Open Ticets":
    tickets = flatten_tickets(fetch_jira_tickets("statusCategory != Done"))
    for t in tickets:
        st.subheader(t['key'])  
        st.write(f"**Summary:** {t['summary']}")
        st.write(f"**Description:** {t['description']}")

elif menu == "Closed Tickets":
    tickets = flatten_tickets(fetch_jira_tickets("statusCategory = Done"))
    for t in tickets:
        st.subheader(t['key'])  
        st.write(f"**Summary:** {t['summary']}")
        st.write(f"**Description:** {t['description']}")

elif menu == "Summarize Ticket":
    ticket_key = st.text_input("Enter Ticket Key to Summarize:")
    if st.button("Summarize"):
        tickets = flatten_tickets(fetch_jira_tickets())
        ticket = next((x for x in tickets if x['key'].lower() == ticket_key.lower()), None)
        if ticket:
            st.write(f"**Summary:** {ticket['summary']}")
            st.write(f"**Description:** {ticket['description']}")
        else:
            st.error("Ticket not found.")

elif menu == "AI Analysis":
    ticket_key = st.text_input("Enter Ticket Key to Analyze:")
    if st.button("Analyze"):
        tickets = flatten_tickets(fetch_jira_tickets())
        ticket = next((x for x in tickets if x['key'].lower() == ticket_key.lower()), None)
        if ticket:
            result = analyze_ticket_lazy(ticket['raw'])
            st.success("AI Suggestion:")
            st.write(result)
        else:
            st.error("Ticket not found.")

elif menu == "Comment":
    ticket_key = st.text_input("Enter Ticket Key to Comment:")
    if st.button("Add Comment"):
        tickets = flatten_tickets(fetch_jira_tickets())
        ticket = next((x for x in tickets if x['key'].lower() == ticket_key.lower()), None)
        if ticket:
            result = analyze_ticket_lazy(ticket['raw'])
            add_comment_to_ticket(ticket['key'], result)
            st.success(f"✅ Comment added to {ticket['key']}")
        else:
            st.error("Ticket not found.")

elif menu =="Suggest Solution":
    ticket_key = st.text_input("Enter Ticket Key for Suggestions:")
    if st.button("Suggest"):
        tickets = flatten_tickets(fetch_jira_tickets())
        ticket = next((x for x in tickets if x['key'].lower() == ticket_key.lower()), None)
        if ticket:
            result = analyze_ticket_lazy(ticket['raw'])
            st.success("📌 Suggested Next Steps:")
            st.write(result)
        else:
            st.error("Ticket not found.")

elif menu == "Auto Assign":
    if st.button("Auto Assign All Unassigned Tickets"):
        auto_assign_all()
        st.success("Auto assignment completed.")

    ticket_key = st.text_input("Or enter a Ticket Key to auto-assign:")
    if st.button("Auto Assign This Ticket"):
        auto_assign_ticket_to_least_loaded(ticket_key)
        st.success(f"Auto-assigned {ticket_key}")

elif menu == "Ask":
    query = st.text_input("Ask a question about tickets:")
    if st.button("Run Query"):
        jql = handle_natural_query(query)
        if jql:
            tickets = flatten_tickets(fetch_jira_tickets(jql))
            if tickets:
                for t in tickets:
                    st.subheader(f"{t['key']} — {t['summary']}")
                    st.write(t['description'])
            else:
                st.warning("No matching tickets found.")
        else:
            st.error("Could not understand your query.")

elif menu == "Refresh":
    st.info("Refreshing ticket data...")
    st.cache_data.clear()
    st.success("Refreshed successfully!")


