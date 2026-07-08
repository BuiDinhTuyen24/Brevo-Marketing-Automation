from predict import predict_segment

lead = {
    "COURSE_1": "Business Intelligence (BI)",
    "COURSE_2": "NONE",
    "COURSE_3": "NONE",
    "COURSE_COUNT": 1,
    "MULTI_COURSE": False,
    "SOURCE_TYPE": "CLUB",
    "SCHOLARSHIP": False,
    "REGISTER_MONTH": 7,
    "REGISTER_DAY_OF_WEEK": "Monday"
}

segment = predict_segment(lead)

print(segment)