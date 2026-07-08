from api.feature_engineering import build_features
from api.predict import predict_segment
from api.database import upsert_lead, update_prediction
from api.brevo import sync_to_brevo


def process_lead(raw_lead: dict):
    features, lead = build_features(raw_lead)

    segment = predict_segment(features)

    lead["segment"] = segment

    upsert_lead(lead)

    update_prediction(
        lead["email"],
        segment
    )

    brevo_result = sync_to_brevo(lead)

    return {
        "status": "success",
        "email": lead["email"],
        "segment": segment,
        "lead": lead,
        "brevo": brevo_result
    }