from supabase import create_client
from api.config import SUPABASE_URL, SUPABASE_KEY
from datetime import datetime

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

MODEL_VERSION = "RandomForest_v1"

def get_unprocessed_raw_leads():
    response = (
        supabase
        .table("raw_leads")
        .select("*")
        .eq("processed", False)
        .execute()
    )
    return response.data


def mark_raw_lead_processed(raw_id: str):
    response = (
        supabase
        .table("raw_leads")
        .update({
            "processed": True,
            "processed_at": datetime.utcnow().isoformat()
        })
        .eq("id", raw_id)
        .execute()
    )
    return response.data


def mark_raw_lead_failed(raw_id: str):
    response = (
        supabase
        .table("raw_leads")
        .update({
            "processed": False
        })
        .eq("id", raw_id)
        .execute()
    )
    return response.data
def insert_lead(data: dict):
    response = (
        supabase
        .table("leads")
        .insert(data)
        .execute()
    )
    return response.data


def upsert_lead(data: dict):
    response = (
        supabase
        .table("leads")
        .upsert(data, on_conflict="email")
        .execute()
    )
    return response.data


def update_prediction(email: str, segment: str):
    response = (
        supabase
        .table("leads")
        .update({
            "segment": segment,
            "prediction_time": datetime.utcnow().isoformat(),
            "model_version": MODEL_VERSION
        })
        .eq("email", email)
        .execute()
    )
    return response.data