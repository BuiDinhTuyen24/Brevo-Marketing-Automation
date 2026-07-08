import requests
from api.config import BREVO_API_KEY

url = "https://api.brevo.com/v3/contacts/lists"

headers = {
    "accept": "application/json",
    "api-key": BREVO_API_KEY
}

response = requests.get(url, headers=headers)

print(response.status_code)
print(response.text)