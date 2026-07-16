from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib

app = FastAPI(title="ScoreSure API")

# Load model
model = joblib.load("scoresure_model.pkl")
encoders = joblib.load("label_encoders.pkl")


class Applicant(BaseModel):
    age: int
    gender: str
    occupation: str
    district: str
    declared_income: float
    electricity_bill: float
    mobile_recharge: float
    existing_loans: int
    repayment_rate: float
    loan_amount: float


@app.get("/")
def home():
    return {"message": "ScoreSure API is Running 🚀"}


@app.post("/predict")
def predict(data: Applicant):

    # Feature Engineering
    estimated_income = max(
        data.declared_income * 0.8,
        data.electricity_bill * 20 + data.mobile_recharge * 10
    )

    income_match = (
        min(data.declared_income, estimated_income)
        / max(data.declared_income, estimated_income)
    ) * 100

    score = (
        data.repayment_rate * 4
        + income_match * 4
        + (100 - data.existing_loans * 20)
    )

    score = max(300, min(900, int(score)))

    df = pd.DataFrame([{
        "age": data.age,
        "gender": data.gender,
        "occupation": data.occupation,
        "district": data.district,
        "declared_income": data.declared_income,
        "electricity_bill": data.electricity_bill,
        "mobile_recharge": data.mobile_recharge,
        "existing_loans": data.existing_loans,
        "repayment_rate": data.repayment_rate,
        "loan_amount": data.loan_amount,
        "estimated_income": estimated_income,
        "income_match": income_match,
        "composite_score": score
    }])

    # Encode categorical values
    for col in ["gender", "occupation", "district"]:
        df[col] = encoders[col].transform(df[col])

    prediction = model.predict(df)

    risk = encoders["risk"].inverse_transform(prediction)[0]

    if risk == "Low":
        decision = "APPROVE"
    elif risk == "Medium":
        decision = "REVIEW"
    else:
        decision = "REJECT"

    # Simple confidence score
    probabilities = model.predict_proba(df)[0]
    confidence = round(max(probabilities) * 100, 2)

    # AI Explanation
    reasons = []

    if data.repayment_rate > 90:
        reasons.append("Excellent repayment history")

    if income_match > 90:
        reasons.append("Income consistency is high")

    if data.existing_loans == 0:
        reasons.append("No existing loans")

    if data.electricity_bill > 700:
        reasons.append("Stable electricity usage")

    return {
        "composite_score": score,
        "risk": risk,
        "decision": decision,
        "estimated_income": round(estimated_income, 2),
        "income_match": round(income_match, 2),
        "confidence": confidence,
        "ai_explanation": reasons
    }