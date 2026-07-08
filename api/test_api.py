import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("BREVO_API_KEY")

url = "https://api.brevo.com/v3/contacts"

headers = {
    "accept": "application/json",
    "api-key": API_KEY
}

response = requests.get(url, headers=headers)

print(response.status_code)
print(response.json())