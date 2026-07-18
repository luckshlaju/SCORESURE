from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import pandas as pd
import numpy as np
import joblib
import traceback
import os

# ==========================================================
# FastAPI
# ==========================================================

app = FastAPI(
    title="ScoreSure AI Loan Assessment API",
    version="3.0"
)

# ==========================================================
# CORS
# ==========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================================
# Project Paths
# ==========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "scoresure_model.pkl")
ENCODER_PATH = os.path.join(BASE_DIR, "label_encoders.pkl")
ACCURACY_PATH = os.path.join(BASE_DIR, "model_accuracy.pkl")

DATASET_PATH = os.path.join(
    BASE_DIR,
    "..",
    "ml",
    "dataset.csv"
)

# ==========================================================
# Load ML Assets
# ==========================================================

try:

    model = joblib.load(MODEL_PATH)

    encoders = joblib.load(ENCODER_PATH)

    if os.path.exists(ACCURACY_PATH):

        model_accuracy = float(joblib.load(ACCURACY_PATH))

    else:

        model_accuracy = 0.0

except Exception as e:

    print(e)

    model = None
    encoders = {}
    model_accuracy = 0.0

# ==========================================================
# Applicant Schema
# ==========================================================

class Applicant(BaseModel):

    age: int

    gender: str

    occupation: str

    district: str

    declared_income: float

    electricity_bill: float

    mobile_recharge: float

    repayment_rate: float

    existing_loans: int

    loan_amount: float

    credit_history_years: int

    payment_defaults: int

    loan_tenure_months: int

# ==========================================================
# Helper
# ==========================================================

def load_dataset():

    print("DATASET PATH =", DATASET_PATH)

    df = pd.read_csv(DATASET_PATH)

    print(df.columns.tolist())

    return df

# ==========================================================
# Home
# ==========================================================

@app.get("/")
def home():

    return {

        "project": "ScoreSure AI Loan Assessment",

        "version": "3.0",

        "status": "Running",

        "model_loaded": model is not None,

        "model_accuracy": model_accuracy,

        "dataset": os.path.basename(DATASET_PATH),

        "endpoints": [

            "/predict",

            "/dashboard",

            "/analytics-dashboard",

            "/history"

        ]

    }
# ==========================================================
# PREDICT
# ==========================================================

@app.post("/predict")
def predict(data: Applicant):

    try:

        if model is None:
            raise HTTPException(
                status_code=500,
                detail="Model not loaded."
            )

        # --------------------------------------------------
        # Feature Engineering
        # --------------------------------------------------

        estimated_income = max(
            data.declared_income * 0.80,
            data.electricity_bill * 18 +
            data.mobile_recharge * 25
        )

        income_match = round(

            min(
                data.declared_income,
                estimated_income
            )

            /

            max(
                data.declared_income,
                estimated_income
            )

            * 100,

            2

        )

        # --------------------------------------------------
        # Create DataFrame
        # --------------------------------------------------

        input_df = pd.DataFrame([{

            "age": data.age,

            "gender": data.gender,

            "occupation": data.occupation,

            "district": data.district,

            "declared_income": data.declared_income,

            "electricity_bill": data.electricity_bill,

            "mobile_recharge": data.mobile_recharge,

            "estimated_income": estimated_income,

            "income_match": income_match,

            "repayment_rate": data.repayment_rate,

            "existing_loans": data.existing_loans,

            "loan_amount": data.loan_amount,

            "credit_history_years": data.credit_history_years,

            "payment_defaults": data.payment_defaults,

            "loan_tenure_months": data.loan_tenure_months

        }])

        # --------------------------------------------------
        # Encode categorical columns
        # --------------------------------------------------

        for col in ["gender", "occupation", "district"]:

            if col in encoders:

                try:

                    input_df[col] = encoders[col].transform(
                        input_df[col]
                    )

                except ValueError:

                    raise HTTPException(
                        status_code=400,
                        detail=f"Unknown value '{input_df[col].iloc[0]}' for {col}."
                    )

        # --------------------------------------------------
        # Prediction
        # --------------------------------------------------

        prediction = model.predict(input_df)[0]

        probabilities = model.predict_proba(input_df)[0]

        confidence = round(
            float(max(probabilities) * 100),
            2
        )

        risk = encoders["risk"].inverse_transform(
            [prediction]
        )[0]

        # --------------------------------------------------
        # Decision
        # --------------------------------------------------

        if risk == "Low Risk":

            decision = "Approved"

        elif risk == "Medium Risk":

            decision = "Manual Review"

        else:

            decision = "Rejected"

        # --------------------------------------------------
        # Composite Score
        # --------------------------------------------------

        score = (

            data.repayment_rate * 4

            +

            income_match * 3

            +

            (100 - data.payment_defaults * 10)

            +

            (100 - data.existing_loans * 10)

            +

            data.credit_history_years * 2

        )

        score = int(
            max(
                300,
                min(
                    900,
                    score
                )
            )
        )

        # --------------------------------------------------
        # Fraud Risk
        # --------------------------------------------------

        if income_match >= 95:

            fraud_risk = "Low"

        elif income_match >= 80:

            fraud_risk = "Medium"

        else:

            fraud_risk = "High"

        # --------------------------------------------------
        # Loan Recommendation
        # --------------------------------------------------

        if score >= 850:

            recommended_loan = int(
                estimated_income * 12
            )

            interest_rate = 8.5

        elif score >= 700:

            recommended_loan = int(
                estimated_income * 8
            )

            interest_rate = 10.5

        else:

            recommended_loan = int(
                estimated_income * 5
            )

            interest_rate = 13.5

        # --------------------------------------------------
        # AI Explanation
        # --------------------------------------------------

        explanation = []

        if data.repayment_rate >= 90:

            explanation.append(
                "Excellent repayment history."
            )

        elif data.repayment_rate >= 70:

            explanation.append(
                "Good repayment history."
            )

        else:

            explanation.append(
                "Poor repayment history."
            )

        if income_match >= 95:

            explanation.append(
                "Declared income matches estimated income."
            )

        elif income_match >= 80:

            explanation.append(
                "Minor variation in income."
            )

        else:

            explanation.append(
                "Large mismatch between declared and estimated income."
            )

        if data.payment_defaults == 0:

            explanation.append(
                "No previous payment defaults."
            )

        else:

            explanation.append(
                f"{data.payment_defaults} previous payment defaults."
            )

        if data.existing_loans <= 1:

            explanation.append(
                "Low debt burden."
            )

        else:

            explanation.append(
                "Multiple existing loans."
            )

        # --------------------------------------------------
        # Suggestions
        # --------------------------------------------------

        suggestions = []

        if data.repayment_rate < 80:

            suggestions.append(
                "Improve repayment behaviour."
            )

        if data.payment_defaults > 0:

            suggestions.append(
                "Avoid future payment defaults."
            )

        if data.existing_loans > 2:

            suggestions.append(
                "Reduce outstanding loans."
            )

        if income_match < 80:

            suggestions.append(
                "Provide additional income proof."
            )

        if len(suggestions) == 0:

            suggestions.append(
                "Maintain current financial behaviour."
            )

        # --------------------------------------------------
        # Save prediction
        # --------------------------------------------------

        df = load_dataset()

        applicant_id = int(df["applicant_id"].max()) + 1

        new_record = {

            "applicant_id": applicant_id,

            "age": data.age,

            "gender": data.gender,

            "occupation": data.occupation,

            "district": data.district,

            "declared_income": data.declared_income,

            "electricity_bill": data.electricity_bill,

            "mobile_recharge": data.mobile_recharge,

            "estimated_income": round(
                estimated_income,
                2
            ),

            "income_match": income_match,

            "repayment_rate": data.repayment_rate,

            "existing_loans": data.existing_loans,

            "loan_amount": data.loan_amount,

            "credit_history_years": data.credit_history_years,

            "payment_defaults": data.payment_defaults,

            "loan_tenure_months": data.loan_tenure_months,

            "risk": risk,

            "decision": decision

        }

        df = pd.concat(
            [
                df,
                pd.DataFrame([new_record])
            ],
            ignore_index=True
        )

        df.to_csv(
            DATASET_PATH,
            index=False
        )

        return {

            "applicant_id": applicant_id,

            "composite_score": score,

            "risk": risk,

            "decision": decision,

            "confidence": confidence,

            "estimated_income": round(
                estimated_income,
                2
            ),

            "income_match": income_match,

            "fraud_risk": fraud_risk,

            "recommended_loan": recommended_loan,

            "interest_rate": interest_rate,

            "ai_explanation": explanation,

            "suggestions": suggestions

        }

    except HTTPException:

        raise

    except Exception as e:

        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
# ==========================================================
# DASHBOARD
# ==========================================================

@app.get("/dashboard")
def dashboard():

    try:

        df = load_dataset()

        # --------------------------------------------------
        # Create decision column if missing
        # --------------------------------------------------

        if "decision" not in df.columns:

            df["decision"] = df["risk"].map({

                "Low Risk": "Approved",

                "Medium Risk": "Manual Review",

                "High Risk": "Rejected"

            })

        # --------------------------------------------------
        # Basic Statistics
        # --------------------------------------------------

        total_applications = len(df)

        approved = int(
            (df["decision"] == "Approved").sum()
        )

        review = int(
            (df["decision"] == "Manual Review").sum()
        )

        rejected = int(
            (df["decision"] == "Rejected").sum()
        )

        average_income = round(
            df["declared_income"].mean(),
            2
        )

        average_repayment = round(
            df["repayment_rate"].mean(),
            2
        )

        average_loan_amount = round(
            df["loan_amount"].mean(),
            2
        )

        average_income_match = round(
            df["income_match"].mean(),
            2
        )
        # --------------------------------------------------
        # Risk Distribution
        # --------------------------------------------------

        risk_distribution = {

            "low": int(
                (df["risk"] == "Low Risk").sum()
            ),

            "medium": int(
                (df["risk"] == "Medium Risk").sum()
            ),

            "high": int(
                (df["risk"] == "High Risk").sum()
            )

        }

        # --------------------------------------------------
        # Decision Distribution
        # --------------------------------------------------

        decision_distribution = {

            "approved": approved,

            "review": review,

            "rejected": rejected

        }

        # --------------------------------------------------
        # Occupation Analysis
        # --------------------------------------------------

        occupation_analysis = (

            df.groupby("occupation")

            .size()

            .sort_values(ascending=False)

            .to_dict()

        )

        # --------------------------------------------------
        # District Analysis
        # --------------------------------------------------

        district_analysis = (

            df.groupby("district")

            .size()

            .sort_values(ascending=False)

            .to_dict()

        )
        # --------------------------------------------------
        # Loan Amount by Risk
        # --------------------------------------------------

        loan_by_risk = (

            df.groupby("risk")["loan_amount"]

            .mean()

            .round(2)

            .to_dict()

        )

        # --------------------------------------------------
        # Repayment by Risk
        # --------------------------------------------------

        repayment_by_risk = (

            df.groupby("risk")["repayment_rate"]

            .mean()

            .round(2)

            .to_dict()

        )

        # --------------------------------------------------
        # Existing Loans Distribution
        # --------------------------------------------------

        existing_loans_distribution = (

            df["existing_loans"]

            .value_counts()

            .sort_index()

            .to_dict()

        )

        # --------------------------------------------------
        # Loan Tenure Distribution
        # --------------------------------------------------

        loan_tenure_distribution = (

            df["loan_tenure_months"]

            .value_counts()

            .sort_index()

            .to_dict()

        )
        # --------------------------------------------------
        # Payment Default Distribution
        # --------------------------------------------------

        payment_default_distribution = (

            df["payment_defaults"]

            .value_counts()

            .sort_index()

            .to_dict()

        )

        # --------------------------------------------------
        # Credit History Distribution
        # --------------------------------------------------

        credit_history_distribution = (

            df["credit_history_years"]

            .value_counts()

            .sort_index()

            .to_dict()

        )

        # --------------------------------------------------
        # Income Match Distribution
        # --------------------------------------------------

        excellent = int(
            (df["income_match"] >= 95).sum()
        )

        good = int(
            (
                (df["income_match"] >= 80)
                &
                (df["income_match"] < 95)
            ).sum()
        )

        poor = int(
            (df["income_match"] < 80).sum()
        )

        income_match_distribution = {

            "Excellent": excellent,

            "Good": good,

            "Poor": poor

        }

        # --------------------------------------------------
        # AI Insights
        # --------------------------------------------------

        ai_insights = {

            "average_income": average_income,

            "average_repayment": average_repayment,

            "average_income_match": average_income_match,

            "average_loan_amount": average_loan_amount,

            "total_loan_processed": int(
                df["loan_amount"].sum()
            ),

            "approval_rate": round(
                approved / total_applications * 100,
                2
            ),

            "high_risk_percentage": round(
                risk_distribution["high"] /
                total_applications * 100,
                2
            )

        }

        # --------------------------------------------------
        # Response
        # --------------------------------------------------

        return {

            "total_applications": total_applications,

            "approved": approved,

            "review": review,

            "rejected": rejected,

            "model_accuracy": model_accuracy,

            "risk_distribution": risk_distribution,

            "decision_distribution": decision_distribution,

            "occupation_analysis": occupation_analysis,

            "district_analysis": district_analysis,

            "loan_by_risk": loan_by_risk,

            "repayment_by_risk": repayment_by_risk,

            "existing_loans_distribution": existing_loans_distribution,

            "loan_tenure_distribution": loan_tenure_distribution,

            "payment_default_distribution": payment_default_distribution,

            "credit_history_distribution": credit_history_distribution,

            "income_match_distribution": income_match_distribution,

            "ai_insights": ai_insights

        }

    except Exception as e:

        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
# ==========================================================
# HISTORY
# ==========================================================

@app.get("/history")
def history():

    try:

        if not os.path.exists(DATASET_PATH):
            raise HTTPException(
                status_code=404,
                detail="Dataset not found."
            )

        df = pd.read_csv(DATASET_PATH)

        if df.empty:
            return {
                "count": 0,
                "history": []
            }

        # Replace NaN with None for JSON
        df = df.where(pd.notnull(df), None)

        history = []

        for _, row in df.iterrows():

            history.append({

                "applicant_id": int(row["applicant_id"]),

                "age": int(row["age"]),

                "gender": row["gender"],

                "occupation": row["occupation"],

                "district": row["district"],

                "declared_income": float(row["declared_income"]),

                "electricity_bill": float(row["electricity_bill"]),

                "mobile_recharge": float(row["mobile_recharge"]),

                "estimated_income": float(row["estimated_income"]),

                "income_match": float(row["income_match"]),

                "repayment_rate": float(row["repayment_rate"]),

                "existing_loans": int(row["existing_loans"]),

                "loan_amount": float(row["loan_amount"]),

                "credit_history_years": int(row["credit_history_years"]),

                "payment_defaults": int(row["payment_defaults"]),

                "loan_tenure_months": int(row["loan_tenure_months"]),

                "risk": row["risk"],

                "decision": row["decision"]

            })

        return {

            "count": len(history),

            "history": history

        }

    except Exception as e:

        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )