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

    # Create DataFrame
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

    # Prediction
    prediction = model.predict(df)[0]
    probabilities = model.predict_proba(df)[0]
    confidence = round(max(probabilities) * 100, 2)

    # Convert numeric prediction back to label
    risk = encoders["risk"].inverse_transform([prediction])[0]

    # Decision
    if risk == "Low":
        decision = "APPROVE"
    elif risk == "Medium":
        decision = "REVIEW"
    else:
        decision = "REJECT"

    # AI Explanation
    reasons = []

    if data.repayment_rate >= 90:
        reasons.append("Excellent repayment history")
    elif data.repayment_rate >= 70:
        reasons.append("Good repayment history")
    else:
        reasons.append("Poor repayment history")

    if income_match >= 95:
        reasons.append("Declared income matches estimated income")
    elif income_match >= 80:
        reasons.append("Income consistency is good")
    else:
        reasons.append("Income mismatch detected")

    if data.existing_loans == 0:
        reasons.append("No existing loans")
    elif data.existing_loans <= 2:
        reasons.append("Manageable existing loans")
    else:
        reasons.append("High number of existing loans")

    if data.electricity_bill < 2500:
        reasons.append("Stable electricity usage")
    else:
        reasons.append("High electricity expenditure")

    # Suggestions
    suggestions = []

    if data.repayment_rate < 80:
        suggestions.append("Improve repayment history")

    if data.existing_loans > 2:
        suggestions.append("Reduce existing loans")

    if data.loan_amount > data.declared_income * 10:
        suggestions.append("Apply for a smaller loan amount")

    if data.declared_income < 25000:
        suggestions.append("Increase verifiable income")

    if len(suggestions) == 0:
        suggestions.append("Maintain your current financial behaviour")

    # Fraud Risk
    if income_match >= 95:
        fraud_risk = "Low"
    elif income_match >= 80:
        fraud_risk = "Medium"
    else:
        fraud_risk = "High"

    # Loan Recommendation
    if score >= 850:
        recommended_loan = int(data.declared_income * 12)
        interest_rate = 8.5
    elif score >= 700:
        recommended_loan = int(data.declared_income * 8)
        interest_rate = 10.5
    else:
        recommended_loan = int(data.declared_income * 5)
        interest_rate = 13.5

    return {
        "composite_score": score,
        "risk": risk,
        "decision": decision,
        "estimated_income": round(estimated_income, 2),
        "income_match": round(income_match, 2),
        "confidence": confidence,
        "fraud_risk": fraud_risk,
        "recommended_loan": recommended_loan,
        "interest_rate": interest_rate,
        "ai_explanation": reasons,
        "suggestions": suggestions
    }
@app.get("/dashboard")
def dashboard():

    import pandas as pd

    df = pd.read_csv("../ml/dataset.csv")

    # Encode categorical columns
    df["gender"] = encoders["gender"].transform(df["gender"])
    df["occupation"] = encoders["occupation"].transform(df["occupation"])
    df["district"] = encoders["district"].transform(df["district"])

    # Feature Engineering
    df["estimated_income"] = df.apply(
        lambda x: max(
            x["declared_income"] * 0.8,
            x["electricity_bill"] * 20 + x["mobile_recharge"] * 10
        ),
        axis=1
    )

    df["income_match"] = (
        df[["declared_income", "estimated_income"]].min(axis=1)
        /
        df[["declared_income", "estimated_income"]].max(axis=1)
    ) * 100

    df["composite_score"] = (
        df["repayment_rate"] * 4
        + df["income_match"] * 4
        + (100 - df["existing_loans"] * 20)
    )

    df["composite_score"] = df["composite_score"].clip(300, 900)

    # Features used by the model

    approved = len(df[df["risk"] == "Low"])
    pending = len(df[df["risk"] == "Medium"])
    rejected = len(df[df["risk"] == "High"])
    average_score = round(df["composite_score"].mean())

    return {
    "total_applications": len(df),

    "approved": int(approved),

    "pending": int(pending),

    "rejected": int(rejected),

    "average_score": average_score,

    "risk_distribution": {
        "low": int(approved),
        "medium": int(pending),
        "high": int(rejected)
    },

    "ai_insights": {
        "avg_repayment": round(df["repayment_rate"].mean(), 2),

        "income_credibility": round(df["income_match"].mean(), 2),

        "high_risk_applicants": int(rejected),

        "loan_processed": int(df["loan_amount"].sum())
    }
}
@app.get("/history")
def history():

    import pandas as pd

    df = pd.read_csv("../ml/dataset.csv")

    history = []

    for _, row in df.iterrows():

        history.append({
            "applicant_id": int(row["applicant_id"]),
            "age": int(row["age"]),
            "gender": row["gender"],
            "occupation": row["occupation"],
            "district": row["district"],
            "income": int(row["declared_income"]),
            "loan_amount": int(row["loan_amount"]),
            "risk": row["risk"],
            "decision": row["decision"]
        })

    return history
from fastapi import HTTPException

@app.get("/analytics")
def analytics():

    try:
        df = pd.read_csv("../ml/dataset.csv")

        # Encode categorical columns
        df["gender"] = encoders["gender"].transform(df["gender"])
        df["occupation"] = encoders["occupation"].transform(df["occupation"])
        df["district"] = encoders["district"].transform(df["district"])

        # Feature Engineering
        df["estimated_income"] = df.apply(
            lambda x: max(
                x["declared_income"] * 0.8,
                x["electricity_bill"] * 20 + x["mobile_recharge"] * 10
            ),
            axis=1
        )

        df["income_match"] = (
            df[["declared_income", "estimated_income"]].min(axis=1)
            /
            df[["declared_income", "estimated_income"]].max(axis=1)
        ) * 100

        df["composite_score"] = (
            df["repayment_rate"] * 4
            + df["income_match"] * 4
            + (100 - df["existing_loans"] * 20)
        )

        df["composite_score"] = df["composite_score"].clip(300, 900)


        X = df[
            [
                "age",
                "gender",
                "occupation",
                "district",
                "declared_income",
                "electricity_bill",
                "mobile_recharge",
                "existing_loans",
                "repayment_rate",
                "loan_amount",
                "estimated_income",
                "income_match",
                "composite_score"
            ]
        ]


        predictions = model.predict(X)

        risks = encoders["risk"].inverse_transform(predictions)

        return {
            "risk_distribution": {
                "low": int((risks == "Low").sum()),
                "medium": int((risks == "Medium").sum()),
                "high": int((risks == "High").sum())
            }
        }


    except Exception as e:
        return {"error": str(e)}