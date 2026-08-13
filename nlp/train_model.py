import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


df = pd.read_csv("dataset/cleaned_reviews.csv")

# Check class distribution
print(df["rating_review"].value_counts())
# -----------------------------
# Load Dataset
# -----------------------------


df = df.dropna(subset=["Clean_Review", "rating_review"])

X = df["Clean_Review"]
y = df["rating_review"]

# -----------------------------
# Load TF-IDF Vectorizer
# -----------------------------

vectorizer = joblib.load("models/tfidf.pkl")

X = vectorizer.transform(X)

# -----------------------------
# Train-Test Split
# -----------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# -----------------------------
# Train Model
# -----------------------------

model = LogisticRegression(
    max_iter=1000,
    random_state=42,
    class_weight="balanced"
)

model.fit(X_train, y_train)
print(f"Training samples: {X_train.shape[0]}")
print(f"Testing samples: {X_test.shape[0]}")
# -----------------------------
# Predictions
# -----------------------------

predictions = model.predict(X_test)

# -----------------------------
# Evaluation
# -----------------------------

print("\nAccuracy:")
print(accuracy_score(y_test, predictions))

print("\nClassification Report:")
print(classification_report(y_test, predictions))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, predictions))

# -----------------------------
# Save Model
# -----------------------------

os.makedirs("models", exist_ok=True)

joblib.dump(model, "models/sentiment_model.pkl")

print("\nModel saved successfully!")