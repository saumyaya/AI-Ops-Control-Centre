import base64
import requests
import streamlit as st

# Secure config from Streamlit secrets
EMAIL = st.secrets["EMAIL"]
API_TOKEN = st.secrets["API_TOKEN"]
DOMAIN = st.secrets["DOMAIN"]
PROJECT_KEY = st.secrets["PROJECT_KEY"]
OLLAMA_MODEL = st.secrets.get("OLLAMA_MODEL", "mistral")
ASSIGNEE_EMAILS = st.secrets.get("ASSIGNEE_EMAILS", [])

# Auth headers
AUTH_STRING = f"{EMAIL}:{API_TOKEN}"
ENCODED_AUTH = base64.b64encode(AUTH_STRING.encode()).decode()

HEADERS = {
    "Authorization": f"Basic {ENCODED_AUTH}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

def get_account_id_by_email(email):
    """Fetch Jira accountId for a given email."""
    url = f"{DOMAIN}/rest/api/3/user/search"
    params = {"query": email}
    response = requests.get(url, headers=HEADERS, params=params)

    if response.status_code != 200:
        st.error(f"❌ Failed to fetch user {email}: {response.status_code}, {response.text}")
        return None

    data = response.json()
    if not data:
        st.warning(f"❌ No user found for email: {email}")
        return None

    return data[0]["accountId"]

def build_assignees():
    """Build and return the assignees mapping only when needed."""
    return {email: get_account_id_by_email(email) for email in ASSIGNEE_EMAILS}
