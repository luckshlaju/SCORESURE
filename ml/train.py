import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import os
import os

import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dataset_path = os.path.join(BASE_DIR, "dataset.csv")

df = pd.read_csv(dataset_path)
print(df.columns.tolist())
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

# Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y      # Keeps the same class distribution
)

# Train Model
model = RandomForestClassifier(
    n_estimators=300,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

# Prediction
y_pred = model.predict(X_test)

# Accuracy
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

model_accuracy = round(accuracy * 100, 2)
print("Model Accuracy (%):", model_accuracy)

# Save Files
os.makedirs("backend", exist_ok=True)

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(BASE_DIR, "..", "backend")

os.makedirs(BACKEND_DIR, exist_ok=True)

joblib.dump(model, os.path.join(BACKEND_DIR, "scoresure_model.pkl"))
joblib.dump(encoders, os.path.join(BACKEND_DIR, "label_encoders.pkl"))
joblib.dump(model_accuracy, os.path.join(BACKEND_DIR, "model_accuracy.pkl"))

print("Model saved successfully!")


