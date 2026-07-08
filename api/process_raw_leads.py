from api.database import (
    get_unprocessed_raw_leads,
    mark_raw_lead_processed
)

from api.pipeline import process_lead

def process_raw_leads():

    raw_leads = get_unprocessed_raw_leads()

    print(f"Found {len(raw_leads)} raw leads.")

    for raw in raw_leads:

        try:

            raw_lead = {
                "register_date": raw["Date"],
                "owner": raw["Mr. KhangNNM"],
                "full_name": raw["Họ và Tên của Leads?"],
                "phone": raw["Số Điện Thoại?"],
                "email": raw["Email?"],
                "course": raw["Bạn quan tâm đến khóa học nào?"],
                "lead_source": raw["Nguồn của Lead?"],
                "scholarship": raw["Ghi chú thêm"] is not None
                and (
                    "học bổng" in raw["Ghi chú thêm"].lower()
                    or "hoc bong" in raw["Ghi chú thêm"].lower()
                    or "scholarship" in raw["Ghi chú thêm"].lower()
                )
            }

            result = process_lead(raw_lead)

            mark_raw_lead_processed(raw["id"])

            print(f"Passed {result['email']} -> {result['segment']}")

        except Exception as e:

            print(f"Error {raw['Email?']} : {e}")


if __name__ == "__main__":
    process_raw_leads()