import joblib
import pandas as pd

model = joblib.load(
    r"D:\Project\Brevo automation\models\random_forest_pipeline.pkl"
)

lead = pd.DataFrame([{
    "COURSE_1": "Business Intelligence (BI)",
    "COURSE_2": "NONE",
    "COURSE_3": "NONE",
    "COURSE_COUNT": 1,
    "MULTI_COURSE": False,
    "SOURCE_TYPE": "CLUB",
    "SCHOLARSHIP": True,
    "REGISTER_MONTH": 7,
    "REGISTER_DAY_OF_WEEK": "Monday"
}])

print(model.predict(lead))