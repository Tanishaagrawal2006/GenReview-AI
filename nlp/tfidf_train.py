import os
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split

# Load cleaned dataset
df = pd.read_csv("dataset/cleaned_reviews.csv")

# Remove missing values
df = df.dropna(subset=["Clean_Review", "rating_review"])

# Features and Labels
X = df["Clean_Review"]
y = df["rating_review"]

# TF-IDF Vectorizer
vectorizer = TfidfVectorizer(
    max_features=5000,
    ngram_range=(1, 2)
)

X_tfidf = vectorizer.fit_transform(X)

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X_tfidf,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Save TF-IDF model
os.makedirs("models", exist_ok=True)
joblib.dump(vectorizer, "models/tfidf.pkl")

print("TF-IDF Vectorizer trained and saved successfully!")
print(f"Training samples: {X_train.shape[0]}")
print(f"Testing samples: {X_test.shape[0]}")
print(f"Vocabulary size: {X_train.shape[1]}")