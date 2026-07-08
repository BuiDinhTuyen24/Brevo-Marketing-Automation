import joblib
import pandas as pd

MODEL_PATH = r"D:\Project\Brevo automation\models\random_forest_pipeline.pkl"

model = joblib.load(MODEL_PATH)


def predict_segment(lead: dict):

    df = pd.DataFrame([lead])

    prediction = model.predict(df)[0]

    return prediction