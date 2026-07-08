from predict import predict_segment
from database import insert_lead, update_prediction

lead = {
    "register_date": "2026-07-08",
    "owner": "Khang",

    "full_name": "Pipeline Test",
    "phone": "0912345678",
    "email": "pipeline3@test.com",

    "lead_source": "AIESEC FTU",

    "course": "Business Intelligence (BI)",

    "course_1": "Business Intelligence (BI)",
    "course_2": "NONE",
    "course_3": "NONE",

    "course_count": 1,
    "multi_course": False,

    "source_type": "CLUB",

    "scholarship": False,

    "register_month": 7,
    "register_day_of_week": "Tuesday",

    "segment": None
}

# B1. Insert lead
insert_lead(lead)

# B2. Predict
segment = predict_segment({
    "COURSE_1": lead["course_1"],
    "COURSE_2": lead["course_2"],
    "COURSE_3": lead["course_3"],
    "COURSE_COUNT": lead["course_count"],
    "MULTI_COURSE": lead["multi_course"],
    "SOURCE_TYPE": lead["source_type"],
    "SCHOLARSHIP": lead["scholarship"],
    "REGISTER_MONTH": lead["register_month"],
    "REGISTER_DAY_OF_WEEK": lead["register_day_of_week"],
})

print("Predicted:", segment)

# B3. Update segment
update_prediction(
    lead["email"],
    segment
)

print("Done.")