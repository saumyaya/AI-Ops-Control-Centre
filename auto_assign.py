import requests
from config import DOMAIN, PROJECT_KEY, HEADERS, ASSIGNEES

def fetch_all_tickets():
    url = f"{DOMAIN}/rest/api/3/search"
    query = {
        "jql": f"project={PROJECT_KEY}",
        "maxResults": 100
    }
    response = requests.get(url, headers=HEADERS, params=query)
    if response.status_code != 200:
        print(f"❌ Error fetching tickets: {response.status_code}, {response.text}")
        return []
    return response.json().get("issues", [])

def get_ticket_counts_by_user():
    tickets = fetch_all_tickets()
    # Reverse ASSIGNEES mapping for easy lookup: {accountId: email}
    account_to_email = {v: k for k, v in ASSIGNEES.items()}
    counts = {email: 0 for email in ASSIGNEES}

    for t in tickets:
        assignee = t.get("fields", {}).get("assignee")
        if assignee and "accountId" in assignee:
            acc_id = assignee["accountId"]
            email = account_to_email.get(acc_id)
            if email:
                counts[email] += 1
    return counts

def pick_least_loaded_user():
    counts = get_ticket_counts_by_user()
    return min(counts, key=counts.get)

def get_account_id(email):
    return ASSIGNEES.get(email)

def assign_ticket(ticket_key, assignee_email):
    account_id = get_account_id(assignee_email)
    url = f"{DOMAIN}/rest/api/3/issue/{ticket_key}/assignee"
    payload = {"accountId": account_id}
    response = requests.put(url, headers=HEADERS, json=payload)
    if response.status_code == 204:
        print(f"✅ Assigned {ticket_key} to {assignee_email}")
    else:
        print(f"❌ Failed to assign {ticket_key}: {response.status_code} {response.text}")

def auto_assign_all():
    tickets = fetch_all_tickets()
    unassigned_tickets = [t for t in tickets if t.get("fields", {}).get("assignee") is None]

    if not unassigned_tickets:
        print("🎉 No unassigned tickets found.")
        return

    for ticket in unassigned_tickets:
        least_loaded_email = pick_least_loaded_user()
        assign_ticket(ticket["key"], least_loaded_email)

def auto_assign_ticket_to_least_loaded(ticket_key):
    least_loaded_email = pick_least_loaded_user()
    assign_ticket(ticket_key, least_loaded_email)
