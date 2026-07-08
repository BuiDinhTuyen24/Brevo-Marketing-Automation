import re
import pandas as pd


def clean_phone(phone):
    if pd.isna(phone):
        return ""

    phone = re.sub(r"\D", "", str(phone))

    if len(phone) == 9:
        phone = "0" + phone

    return phone


def clean_phone(phone):
    if pd.isna(phone):
        return ""

    phone = re.sub(r"\D", "", str(phone))

    # 912345678 -> 84912345678
    if len(phone) == 9:
        phone = "84" + phone

    # 0912345678 -> 84912345678
    elif phone.startswith("0"):
        phone = "84" + phone[1:]

    # +84912345678 -> 84912345678
    elif phone.startswith("+84"):
        phone = phone[1:]

    return phone


def get_source_type(source):
    if pd.isna(source):
        return "OTHER"

    source = str(source).lower()

    if any(k in source for k in ["aiesec", "clb", "club", "workshop", "seminar", "event"]):
        return "CLUB"

    if any(k in source for k in ["neu", "vnu", "ueb", "ftu", "hust", "trường", "đại học"]):
        return "UNIVERSITY"

    if any(k in source for k in ["facebook", "zalo", "tiktok", "instagram", "social"]):
        return "SOCIAL"

    return "OTHER"


def split_courses(course):
    if pd.isna(course):
        courses = []
    else:
        courses = [c.strip() for c in str(course).split(",")]

    while len(courses) < 3:
        courses.append("NONE")

    course_count = len([c for c in courses if c != "NONE"])

    return {
        "course_1": courses[0],
        "course_2": courses[1],
        "course_3": courses[2],
        "course_count": course_count,
        "multi_course": course_count > 1
    }


def build_features(raw_lead: dict):
    courses = split_courses(raw_lead["course"])

    register_date = pd.to_datetime(raw_lead["register_date"])

    source_type = get_source_type(raw_lead["lead_source"])

    features = {
        "COURSE_1": courses["course_1"],
        "COURSE_2": courses["course_2"],
        "COURSE_3": courses["course_3"],
        "COURSE_COUNT": courses["course_count"],
        "MULTI_COURSE": courses["multi_course"],
        "SOURCE_TYPE": source_type,
        "SCHOLARSHIP": raw_lead["scholarship"],
        "REGISTER_MONTH": register_date.month,
        "REGISTER_DAY_OF_WEEK": register_date.day_name()
    }

    db_data = {
        "register_date": raw_lead["register_date"],
        "owner": raw_lead["owner"],
        "full_name": raw_lead["full_name"],
        "phone": clean_phone(raw_lead["phone"]),
        "email": raw_lead["email"],
        "lead_source": raw_lead["lead_source"],
        "course": raw_lead["course"],
        "course_1": courses["course_1"],
        "course_2": courses["course_2"],
        "course_3": courses["course_3"],
        "course_count": courses["course_count"],
        "multi_course": courses["multi_course"],
        "source_type": source_type,
        "scholarship": raw_lead["scholarship"],
        "register_month": register_date.month,
        "register_day_of_week": register_date.day_name()
    }

    return features, db_data