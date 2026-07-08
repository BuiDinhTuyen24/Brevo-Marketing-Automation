import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("BREVO_API_KEY")

url = "https://api.brevo.com/v3/contacts"

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "api-key": API_KEY
}

payload = {
    "email": "test_mcna@example.com",
    "attributes": {
        "FIRSTNAME": "Test",
        "COURSE": "AI Agent",
        "LEAD_SOURCE": "API",
        "LEAD_TYPE": "Hot",
        "OWNER": "Khang",
        "SCHOLARSHIP": False
    },
    "updateEnabled": True
}

response = requests.post(url, headers=headers, json=payload)

print(response.status_code)
print(response.text)

