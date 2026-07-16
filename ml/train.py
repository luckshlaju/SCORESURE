import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Load dataset
df = pd.read_csv("ml/dataset/dataset.csv")

# Encode categorical columns
encoders = {}
categorical_cols = ["gender", "occupation", "district", "risk", "decision"]

for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    encoders[col] = le

# Features
X = df.drop(columns=["risk", "decision", "applicant_id"])

# Target
y = df["risk"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)

# Train model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# Prediction
y_pred = model.predict(X_test)

# Accuracy
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

import os

os.makedirs("backend", exist_ok=True)

joblib.dump(model, "backend/scoresure_model.pkl")
joblib.dump(encoders, "backend/label_encoders.pkl")

print("Model saved successfully!")