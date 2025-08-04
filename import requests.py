import requests
from requests.auth import HTTPBasicAuth

# Replace with your details
EMAIL = "saumya046btece22@igdtuw.ac.in"
API_TOKEN = "************"
DOMAIN = "https://igdtuw-team-lznfyyiz.atlassian.net"

url = f"{DOMAIN}/rest/api/3/myself"

response = requests.get(
    url,
    auth=HTTPBasicAuth(EMAIL, API_TOKEN),
    headers={"Accept": "application/json"}
)

print("Status Code:", response.status_code)
print("Response:", response.json())
