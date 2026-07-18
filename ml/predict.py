import pandas as pd
import joblib

# Load model and encoders
model = joblib.load("backend/scoresure_model.pkl")
encoders = joblib.load("backend/label_encoders.pkl")


# -----------------------------
# Applicant Data
# -----------------------------

applicant = {

    "age": 32,

    "gender": "Female",

    "occupation": "Teacher",

    "district": "Coimbatore",

    "declared_income": 45000,

    "electricity_bill": 1400,

    "mobile_recharge": 500,

    "repayment_rate": 85,

    "existing_loans": 1,

    "loan_amount": 150000,

    "credit_history_years": 6,

    "payment_defaults": 0,

    "loan_tenure_months": 36

}

# -----------------------------
# Feature Engineering
# -----------------------------

estimated_income = max(

    applicant["declared_income"] * 0.80,

    applicant["electricity_bill"] * 18 +
    applicant["mobile_recharge"] * 25

)


income_match = (

    min(
        applicant["declared_income"],
        estimated_income
    )
    /
    max(
        applicant["declared_income"],
        estimated_income
    )

) * 100



# -----------------------------
# Create Model Input
# -----------------------------

df = pd.DataFrame([{

    "age": applicant["age"],

    "gender": applicant["gender"],

    "occupation": applicant["occupation"],

    "district": applicant["district"],


    "declared_income":
        applicant["declared_income"],


    "electricity_bill":
        applicant["electricity_bill"],


    "mobile_recharge":
        applicant["mobile_recharge"],


    "estimated_income":
        estimated_income,


    "income_match":
        income_match,


    "repayment_rate":
        applicant["repayment_rate"],


    "existing_loans":
        applicant["existing_loans"],


    "loan_amount":
        applicant["loan_amount"],


    "credit_history_years":
        applicant["credit_history_years"],


    "payment_defaults":
        applicant["payment_defaults"],


    "loan_tenure_months":
        applicant["loan_tenure_months"]

}])


# -----------------------------
# Encode Categorical Features
# -----------------------------

for col in ["gender", "occupation", "district"]:

    df[col] = encoders[col].transform(df[col])


# -----------------------------
# Prediction
# -----------------------------

prediction = model.predict(df)[0]


probability = model.predict_proba(df)[0]


confidence = max(probability) * 100


risk = encoders["risk"].inverse_transform(
    [prediction]
)[0]


# -----------------------------
# Decision
# -----------------------------

if risk == "Low Risk":

    decision = "APPROVED"


elif risk == "Medium Risk":

    decision = "MANUAL REVIEW"


else:

    decision = "REJECTED"



# -----------------------------
# AI Explanation
# -----------------------------

reasons = []


if applicant["repayment_rate"] >= 90:

    reasons.append(
        "Excellent repayment history"
    )


elif applicant["repayment_rate"] >= 70:

    reasons.append(
        "Good repayment history"
    )


else:

    reasons.append(
        "Poor repayment history"
    )


if income_match >= 95:

    reasons.append(
        "Declared income matches estimated income"
    )

elif income_match >= 80:

    reasons.append(
        "Minor income variation detected"
    )

else:

    reasons.append(
        "Large income mismatch detected"
    )


if applicant["payment_defaults"] == 0:

    reasons.append(
        "No previous payment defaults"
    )


if applicant["existing_loans"] <= 1:

    reasons.append(
        "Low debt burden"
    )


# -----------------------------
# Final Report
# -----------------------------

print("="*40)

print("SCORESURE AI REPORT")

print("="*40)


print(
    "Risk Level      :",
    risk
)


print(
    "Decision        :",
    decision
)


print(
    "Confidence      : {:.2f}%".format(confidence)
)


print(
    "Estimated Income:",
    round(estimated_income,2)
)


print(
    "Income Match    : {:.2f}%".format(income_match)
)


print("\nAI Explanation")

for r in reasons:
    print("•", r)