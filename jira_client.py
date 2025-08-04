import requests
from requests.auth import HTTPBasicAuth
from config import EMAIL, API_TOKEN, DOMAIN, PROJECT_KEY

def fetch_jira_tickets():
    url = f"{DOMAIN}/rest/api/3/search"
    params = {"jql": f"project={PROJECT_KEY}", "maxResults": 10}
    response = requests.get(
        url,
        params=params,
        auth=HTTPBasicAuth(EMAIL, API_TOKEN),
        headers={"Accept": "application/json"}
    )
    return [
        {
            "key": i["key"],
            "summary": i["fields"]["summary"],
            "description": i["fields"].get("description", "")
        } for i in response.json().get("issues", [])
    ]

def post_comment(issue_key, comment):
    url = f"{DOMAIN}/rest/api/3/issue/{issue_key}/comment"
    payload = {"body": comment}
    requests.post(
        url,
        json=payload,
        auth=HTTPBasicAuth(EMAIL, API_TOKEN),
        headers={"Accept": "application/json", "Content-Type": "application/json"}
    )
