import pandas as pd
import joblib

# Load model and encoders
model = joblib.load("backend/scoresure_model.pkl")
encoders = joblib.load("backend/label_encoders.pkl")
# -----------------------------
# Applicant Data
# -----------------------------
applicant = {
    "age": 30,
    "gender": "Male",
    "occupation": "Farmer",
    "district": "Chennai",
    "declared_income": 20000,
    "electricity_bill": 850,
    "mobile_recharge": 299,
    "existing_loans": 1,
    "repayment_rate": 95,
    "loan_amount": 50000
}

# -----------------------------
# Feature Engineering
# -----------------------------

# Estimate income
estimated_income = (
    applicant["electricity_bill"] * 20
    + applicant["mobile_recharge"] * 10
)

estimated_income = max(
    estimated_income,
    applicant["declared_income"] * 0.8
)

income_match = (
    min(applicant["declared_income"], estimated_income)
    / max(applicant["declared_income"], estimated_income)
) * 100

# Composite Score

score = (
    applicant["repayment_rate"] * 4
    + income_match * 4
    + (100 - applicant["existing_loans"] * 20)
)

score = max(300, min(900, int(score)))

# Prepare dataframe

df = pd.DataFrame([{
    **applicant,
    "estimated_income": estimated_income,
    "income_match": income_match,
    "composite_score": score
}])

# Encode

for col in ["gender","occupation","district"]:
    df[col] = encoders[col].transform(df[col])

# Predict

prediction = model.predict(df)

risk = encoders["risk"].inverse_transform(prediction)[0]

# Loan Decision

if risk == "Low":
    decision = "APPROVE"

elif risk == "Medium":
    decision = "REVIEW"

else:
    decision = "REJECT"

# AI Explanation

reasons = []

if applicant["repayment_rate"] > 90:
    reasons.append("Excellent repayment history")

if income_match > 90:
    reasons.append("Declared income matches estimated income")

if applicant["existing_loans"] == 0:
    reasons.append("No existing loans")

if applicant["electricity_bill"] > 700:
    reasons.append("Stable electricity usage pattern")

# -----------------------------
# Final Output
# -----------------------------

print("="*40)

print("SCORESURE AI REPORT")

print("="*40)

print("Composite Score :", score)

print("Risk Level      :", risk)

print("Decision        :", decision)

print("Estimated Income:", int(estimated_income))

print("Income Match    : {:.2f}%".format(income_match))

print("\nAI Explanation")

for r in reasons:
    print("•", r)