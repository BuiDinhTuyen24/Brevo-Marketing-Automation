from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

from api.predict import predict_segment
from api.database import upsert_lead, update_prediction
from api.brevo import sync_to_brevo
from api.feature_engineering import build_features
from api.pipeline import process_lead

app = FastAPI()


class LeadRequest(BaseModel):
    register_date: str
    owner: str
    full_name: str
    phone: str
    email: str
    lead_source: str
    course: str
    scholarship: bool = False


@app.post("/lead")
def create_lead(lead: LeadRequest):
    raw_lead = lead.model_dump()

    result = process_lead(raw_lead)

    return result