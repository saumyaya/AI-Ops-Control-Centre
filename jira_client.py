import requests
from requests.auth import HTTPBasicAuth
from config import EMAIL, API_TOKEN, DOMAIN, PROJECT_KEY

def fetch_jira_tickets(jql_filter=""):
    url = f"{DOMAIN}/rest/api/3/search"
    jql = f"project={PROJECT_KEY}"
    if jql_filter:
        jql += f" AND {jql_filter}"

    params = {"jql": jql, "maxResults": 58}
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
def add_comment_to_ticket(issue_key, comment_body):
    url = f"{DOMAIN}/rest/api/3/issue/{issue_key}/comment"

    payload = {
        "body": {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "text": comment_body
                        }
                    ]
                }
            ]
        }
    }

    response = requests.post(
        url,
        json=payload,
        auth=HTTPBasicAuth(EMAIL, API_TOKEN),
        headers={"Accept": "application/json", "Content-Type": "application/json"}
    )

    if response.status_code == 201:
        print(f"✅ Comment added to {issue_key}")
    else:
        print(f"❌ Failed to add comment to {issue_key}: {response.status_code}")
        print(response.text)


