import pandas as pd
import re
import io
import sys

# Khắc phục lỗi terminal hiển thị tiếng Việt (nếu cần)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

df = pd.read_csv(
    r"D:\Project\Brevo automation\data\raw\2026-07-06 1000 leads - Sheet1.csv",
    encoding="utf-8-sig"
)

# Xóa khoảng trắng ở tên cột
df.columns = df.columns.str.strip()

def clean_phone(phone):
    if pd.isna(phone):
        return ""

    phone = re.sub(r"\D", "", str(phone))

    # 912345678 -> 0912345678
    if len(phone) == 9:
        phone = "0" + phone

    # 0912345678 -> 84912345678
    if phone.startswith("0"):
        phone = "84" + phone[1:]

    # +84912345678 -> 84912345678
    if phone.startswith("+84"):
        phone = phone[1:]

    return phone

def get_source_type(source):
    if pd.isna(source):
        return "OTHER"
    source = str(source).lower()
    club_keywords = ["aiesec", "clb", "club", "workshop", "seminar", "event"]
    if any(k in source for k in club_keywords):
        return "CLUB"
    university_keywords = ["neu", "vnu", "ueb", "ftu", "hust", "trường", "đại học"]
    if any(k in source for k in university_keywords):
        return "UNIVERSITY"
    if any(k in source for k in ["facebook", "zalo", "tiktok", "instagram", "social"]):
        return "SOCIAL"
    return "OTHER"

# --- HÀM MỚI: Chuyển đổi tên khóa học sang dạng viết tắt ---
def get_course_code(course_name):
    if pd.isna(course_name):
        return "OTHER"
    
    course_name = str(course_name).upper()
    
    if "BUSINESS INTELLIGENCE" in course_name or "BI" in course_name:
        return "BI"
    elif "BUSINESS ANALYST" in course_name or "BA" in course_name:
        return "BA"
    elif "DATA ANALYST" in course_name or "DA" in course_name:
        return "DA"
    elif "GENAI" in course_name or "GENERATIVE AI" in course_name:
        return "GENAI"
    elif "AI AGENT" in course_name or "AGENT" in course_name:
        return "AI_AGENT"
    
    return "COURSE"

df["Số Điện Thoại?"] = df["Số Điện Thoại?"].apply(clean_phone)

# Đổi tên cột theo Brevo
df = df.rename(columns={
    "Date": "REGISTER_DATE",
    "Mr. KhangNNM": "OWNER",
    "Họ và Tên của Leads?": "FIRSTNAME",
    "Số Điện Thoại?": "SMS",
    "Email?": "EMAIL",
    "Nguồn của Lead?": "LEAD_SOURCE",
    "Bạn quan tâm đến khóa học nào?": "COURSE",
    "Loại LEADS?": "LEAD_TYPE"
})

# Tạo Scholarship
df["SCHOLARSHIP"] = (
    df["Ghi chú thêm"]
    .fillna("")
    .str.lower()
    .str.contains("học bổng|hoc bong|scholarship", regex=True)
)

def split_courses(course):
    if pd.isna(course):
        return pd.Series([None, None, None, 0, False])
    courses = [c.strip() for c in str(course).split(",")]
    while len(courses) < 3:
        courses.append(None)
    return pd.Series([
        courses[0],
        courses[1],
        courses[2],
        len([c for c in courses if c is not None]),
        len([c for c in courses if c is not None]) > 1
    ])

# Feature Engineering
df[["COURSE_1", "COURSE_2", "COURSE_3", "COURSE_COUNT", "MULTI_COURSE"]] = df["COURSE"].apply(split_courses)
df["MULTI_COURSE"] = df["COURSE_COUNT"] > 1
df["REGISTER_DATE"] = pd.to_datetime(df["REGISTER_DATE"])
df["REGISTER_MONTH"] = df["REGISTER_DATE"].dt.month
df["REGISTER_DAY_OF_WEEK"] = df["REGISTER_DATE"].dt.day_name()

df["SOURCE_TYPE"] = df["LEAD_SOURCE"].apply(get_source_type)

# --- CẬP NHẬT: Tạo SEGMENT theo định dạng chuẩn hóa ---
df["SEGMENT"] = df["COURSE_1"].apply(get_course_code) + "_" + df["SOURCE_TYPE"]

# Chỉ giữ các cột cần import
ml_df = df[["EMAIL", "REGISTER_DATE", "COURSE_1", "COURSE_2", "COURSE_3", "COURSE_COUNT", "MULTI_COURSE", "SOURCE_TYPE", "SCHOLARSHIP", "REGISTER_MONTH", "REGISTER_DAY_OF_WEEK", "SEGMENT"]]
brevo_df = df[["EMAIL", "FIRSTNAME", "SMS", "OWNER", "REGISTER_DATE", "LEAD_SOURCE", "COURSE", "SCHOLARSHIP", "SEGMENT"]]

print(ml_df.columns.tolist())
print(brevo_df.columns.tolist())
print("\nThống kê SEGMENT thực tế:")
print(ml_df["SEGMENT"].value_counts())

# Xuất CSV
ml_df.to_csv(r"D:\Project\Brevo automation\data\processed\ml_dataset.csv", index=False, encoding="utf-8-sig")
brevo_df.to_csv(r"D:\Project\Brevo automation\data\processed\brevo_import.csv", index=False, encoding="utf-8-sig")