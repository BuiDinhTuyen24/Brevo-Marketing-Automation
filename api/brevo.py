import requests
from api.config import BREVO_API_KEY

BREVO_CONTACT_URL = "https://api.brevo.com/v3/contacts"

LIST_MAPPING = {
    "BI_CLUB": 10,
    "BI_UNIVERSITY": 11,
    "BA_SOCIAL": 12,
    "BA_OTHER": 13,
    "AI_AGENT_CLUB": 14,
    "DA_OTHER": 15,
    "GENAI_UNIVERSITY": 16,
    "DA_CLUB": 17
}

AI_LIST_IDS = list(LIST_MAPPING.values())


def sync_to_brevo(lead: dict):
    segment = lead["segment"]
    list_id = LIST_MAPPING.get(segment)

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "api-key": BREVO_API_KEY
    }

    payload = {
        "email": lead["email"],
        "attributes": {
            "FIRSTNAME": lead["full_name"],
            "SMS": lead["phone"],
            "OWNER": lead["owner"],
            "COURSE": lead["course"],
            "LEAD_SOURCE": lead["lead_source"],
            "SOURCE_TYPE": lead["source_type"],
            "SCHOLARSHIP": lead["scholarship"],
            "SEGMENT": segment
        },
        "updateEnabled": True
    }

    create_res = requests.post(
        BREVO_CONTACT_URL,
        headers=headers,
        json=payload
    )

    remove_payload = {
        "emails": [lead["email"]]
    }

    remove_results = []

    for old_list_id in AI_LIST_IDS:
        remove_res = requests.post(
            f"https://api.brevo.com/v3/contacts/lists/{old_list_id}/contacts/remove",
            headers=headers,
            json=remove_payload
        )

        remove_results.append({
            "list_id": old_list_id,
            "status_code": remove_res.status_code,
            "response": remove_res.text
        })

    add_result = None

    if list_id:
        add_payload = {
            "emails": [lead["email"]]
        }

        add_res = requests.post(
            f"https://api.brevo.com/v3/contacts/lists/{list_id}/contacts/add",
            headers=headers,
            json=add_payload
        )

        add_result = {
            "list_id": list_id,
            "status_code": add_res.status_code,
            "response": add_res.text
        }

    return {
        "contact": {
            "status_code": create_res.status_code,
            "response": create_res.text
        },
        "removed_from_ai_lists": remove_results,
        "added_to_segment_list": add_result
    }