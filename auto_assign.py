import requests
import streamlit as st
from config import DOMAIN, PROJECT_KEY, HEADERS, build_assignees

def fetch_all_tickets():
    """Fetch all tickets from Jira."""
    url = f"{DOMAIN}/rest/api/3/search"
    params = {"jql": f"project={PROJECT_KEY}", "maxResults": 100}
    response = requests.get(url, headers=HEADERS, params=params)
    return response.json().get("issues", [])

def auto_assign_all():
    """Assign all unassigned tickets to least-loaded users."""
    tickets = fetch_all_tickets()
    assignees = build_assignees()  # Lazy load here
    if not assignees:
        st.error("❌ No valid assignees found.")
        return

    # Initialize load counts for each user
    user_load = {user: 0 for user in assignees.values()}

    for t in tickets:
        if not t["fields"].get("assignee"):
            least_loaded = min(user_load, key=user_load.get)
            assign_ticket(t["key"], least_loaded)
            user_load[least_loaded] += 1
            st.success(f"✅ Assigned {t['key']} to {least_loaded}")

def assign_ticket(ticket_key, account_id):
    """Assign a Jira ticket to a specific account ID."""
    url = f"{DOMAIN}/rest/api/3/issue/{ticket_key}/assignee"
    payload = {"accountId": account_id}
    response = requests.put(url, headers=HEADERS, json=payload)
    if response.status_code == 204:
        return True
    st.error(f"❌ Failed to assign {ticket_key}: {response.status_code}, {response.text}")
    return False

def get_ticket_counts_by_user():
    """Count tickets assigned to each user."""
    tickets = fetch_all_tickets()
    assignees = build_assignees()
    account_to_email = {v: k for k, v in assignees.items()}
    counts = {email: 0 for email in assignees}

    for t in tickets:
        assignee = t.get("fields", {}).get("assignee")
def get_ticket_counts_by_user():
    return counts

def pick_least_loaded_user():
    """Pick the user with the least ticket load."""
    assignees = build_assignees()
    counts = get_ticket_counts_by_user()
    return min(counts, key=counts.get) if counts else None

def get_account_id(email):
    """Get Jira accountId from email."""
    assignees = build_assignees()
    return assignees.get(email)

def auto_assign_ticket_to_least_loaded(ticket_key):
    """Assign a ticket to the least-loaded user."""
    assignees = build_assignees()
    least_loaded_email = pick_least_loaded_user()
    if least_loaded_email:
        account_id = assignees.get_account_id(least_loaded_email)
        if account_id:
            assign_ticket(ticket_key, account_id)

