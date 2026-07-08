from database import insert_lead

lead = {
    "full_name": "Test User",
    "email": "test@example.com",
    "phone": "0912345678",
    "course": "AI Agent",
    "lead_source": "Facebook",
    "lead_type": "Hot",
    "scholarship": False
}

print(insert_lead(lead))