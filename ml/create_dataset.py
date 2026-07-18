import pandas as pd
import numpy as np

# ----------------------------
# Random seed for reproducibility
# ----------------------------
np.random.seed(42)

# ----------------------------
# Load Dataset
# ----------------------------
df = pd.read_csv("ml/data.csv")

# ----------------------------
# Remove rows with missing MonthlyIncome
# ----------------------------
df = df.dropna(subset=["MonthlyIncome"])

# ----------------------------
# Applicant ID
# ----------------------------
df["applicant_id"] = range(1, len(df) + 1)

# ----------------------------
# Basic Fields
# ----------------------------
df["age"] = df["age"]
df["gender"] = "Unknown"
# Gender
df["gender"] = np.random.choice(
    ["Male", "Female"],
    size=len(df),
    p=[0.52, 0.48]
)

# District
districts = [
    "Chennai",
    "Coimbatore",
    "Madurai",
    "Salem",
    "Trichy",
    "Erode",
    "Vellore",
    "Tirunelveli",
    "Thanjavur",
    "Thoothukudi"
]

df["district"] = np.random.choice(
    districts,
    size=len(df)
)

# ----------------------------
# Income
# ----------------------------
df["declared_income"] = df["MonthlyIncome"]


# =====================================================
# Occupation (derived from age and income)
# =====================================================

def assign_occupation(age, income):

    if age <= 22:
        if income < 20000:
            return "Student"
        elif income < 40000:
            return "Intern"
        else:
            return "Software Engineer"

    elif age <= 30:
        if income < 25000:
            return "Laborer"
        elif income < 50000:
            return "Sales Executive"
        elif income < 80000:
            return "Teacher"
        elif income < 120000:
            return "Software Engineer"
        else:
            return "Business"

    elif age <= 45:
        if income < 30000:
            return "Driver"
        elif income < 60000:
            return "Government Employee"
        elif income < 100000:
            return "Manager"
        elif income < 150000:
            return "Doctor"
        else:
            return "Business"

    else:
        if income < 30000:
            return "Farmer"
        elif income < 60000:
            return "Government Employee"
        elif income < 120000:
            return "Business"
        else:
            return "Retired"

df["occupation"] = df.apply(
    lambda x: assign_occupation(x["age"], x["declared_income"]),
    axis=1
)
# ----------------------------
# Existing Loans
# ----------------------------
df["existing_loans"] = df["NumberOfOpenCreditLinesAndLoans"]

# ----------------------------
# Payment Defaults
# ----------------------------
df["payment_defaults"] = df["NumberOfTimes90DaysLate"]

# ----------------------------
# Loan Amount (Estimated)
# ----------------------------
df["loan_amount"] = (
    df["declared_income"] *
    (1 + df["DebtRatio"].clip(0, 2))
).round(2)

# ----------------------------
# Credit History (Estimated)
# ----------------------------
df["credit_history_years"] = (
    (df["age"] - 18) * 0.4
).clip(lower=1, upper=35).astype(int)

# ----------------------------
# Loan Tenure
# ----------------------------
def tenure(amount):
    if amount < 50000:
        return 12
    elif amount < 150000:
        return 24
    elif amount < 300000:
        return 36
    elif amount < 500000:
        return 48
    return 60

df["loan_tenure_months"] = df["loan_amount"].apply(tenure)

# ----------------------------
# Alternative Data Features
# ----------------------------
df["electricity_bill"] = (
    df["declared_income"] * 0.035
).round(2)

df["mobile_recharge"] = (
    200 +
    (df["declared_income"] / 1000) * 15
).clip(200, 1200).round()

# ----------------------------
# Estimated Income
# ----------------------------
df["estimated_income"] = df.apply(
    lambda x: max(
        x["declared_income"] * 0.80,
        x["electricity_bill"] * 18 +
        x["mobile_recharge"] * 25
    ),
    axis=1
)

# ----------------------------
# Income Match
# ----------------------------
df["income_match"] = (
    df[["declared_income", "estimated_income"]].min(axis=1)
    /
    df[["declared_income", "estimated_income"]].max(axis=1)
) * 100

df["income_match"] = df["income_match"].round(2)

# ----------------------------
# Repayment Rate
# ----------------------------
df["repayment_rate"] = (
    100
    - df["payment_defaults"] * 10
    - df["DebtRatio"] * 5
).clip(30, 100).round(2)
# ----------------------------
# Risk Label
# ----------------------------
def get_risk(default):
    if default == 1:
        return "High Risk"
    elif default > 0:
        return "Medium Risk"
    else:
        return "Low Risk"

df["risk"] = df["SeriousDlqin2yrs"].apply(get_risk)

# ----------------------------
# Decision
# ----------------------------
def get_decision(risk):
    if risk == "Low Risk":
        return "Approved"
    elif risk == "Medium Risk":
        return "Manual Review"
    else:
        return "Rejected"

df["decision"] = df["risk"].apply(get_decision)

# ----------------------------
# Final Dataset
# ----------------------------
final_df = df[
    [
        "applicant_id",
        "age",
        "gender",
        "occupation",
        "district",
        "declared_income",
        "electricity_bill",
        "mobile_recharge",
        "estimated_income",
        "income_match",
        "repayment_rate",
        "existing_loans",
        "loan_amount",
        "credit_history_years",
        "payment_defaults",
        "loan_tenure_months",
        "risk",
        "decision"
    ]
]

# ----------------------------
# Save Processed Dataset
# ----------------------------
final_df.to_csv("ml/scoresure_dataset.csv", index=False)

print("===================================")
print(" ScoreSure dataset created!")
print(" Saved as: ml/scoresure_dataset.csv")
print(" Total Records:", len(final_df))
print("===================================")