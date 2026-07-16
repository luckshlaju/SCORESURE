import pandas as pd
import joblib
import shap
import matplotlib.pyplot as plt

# Load model
model = joblib.load("scoresure_model.pkl")

# Load dataset
df = pd.read_csv("ml/dataset/dataset.csv")

# Load encoders
encoders = joblib.load("label_encoders.pkl")

# Encode categorical columns
for col in ["gender", "occupation", "district", "risk", "decision"]:
    df[col] = encoders[col].transform(df[col])

# Features
X = df.drop(columns=["risk", "decision", "applicant_id"])

# SHAP Explainer
explainer = shap.TreeExplainer(model)

# SHAP values
shap_values = explainer.shap_values(X)

# Feature Importance Plot
shap.summary_plot(
    shap_values,
    X,
    plot_type="bar",
    show=True
)