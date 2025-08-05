import base64
import requests
EMAIL = "your-email@example.com"
API_TOKEN = "your-jira-api-token"
DOMAIN = "https://your-domain.atlassian.net"
PROJECT_KEY = "your project key"  
OLLAMA_MODEL = "mistral"
AUTH_STRING = f"{EMAIL}:{API_TOKEN}"
ENCODED_AUTH = base64.b64encode(AUTH_STRING.encode()).decode()

HEADERS = {
    "Authorization": f"Basic {ENCODED_AUTH}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}


def get_account_id_by_email(email):
    url = f"{DOMAIN}/rest/api/3/user/search"
    params = {"query": email}
    response = requests.get(url, headers=HEADERS, params=params)

    if response.status_code != 200:
        print(f"❌ Failed to fetch user: {response.status_code}, {response.text}")
        return None

    data = response.json()
    if not data:
        print(f"❌ No user found for email: {email}")
        return None

    return data[0]["accountId"]

ASSIGNEE_EMAILS = ["your-email1@example.com", "your-email2@example.com"]

ASSIGNEES = {
    email: get_account_id_by_email(email)
    for email in ASSIGNEE_EMAILS
}
