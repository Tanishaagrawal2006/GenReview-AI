import re
import joblib
import nltk
import pandas as pd
from nltk.corpus import stopwords

# Download stopwords (only first time)
nltk.download("stopwords")

# Load stopwords
stop_words = set(stopwords.words("english"))

# -----------------------------
# Load Saved Models
# -----------------------------

vectorizer = joblib.load("models/tfidf.pkl")
model = joblib.load("models/sentiment_model.pkl")

# -----------------------------
# Preprocessing Function
# -----------------------------

def clean_text(text):
    if pd.isna(text):
        return ""

    # Convert to lowercase
    text = text.lower()

    # Remove punctuation, numbers and special characters
    text = re.sub(r'[^a-z\s]', '', text)

    # Remove stopwords
    words = text.split()
    words = [word for word in words if word not in stop_words]

    return " ".join(words)

# -----------------------------
# Prediction Function
# -----------------------------

def predict_sentiment(review):
    cleaned_review = clean_text(review)

    review_vector = vectorizer.transform([cleaned_review])

    prediction = model.predict(review_vector)[0]

    return prediction

# -----------------------------
# Test
# -----------------------------

if __name__ == "__main__":
    review = input("Enter a review: ")

    sentiment = predict_sentiment(review)

    print(f"\nPredicted Sentiment: {sentiment}")