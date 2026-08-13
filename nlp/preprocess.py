import pandas as pd
import re
import nltk
from nltk.corpus import stopwords

# Download stopwords (only first time)
nltk.download("stopwords")

# Load dataset
df = pd.read_excel("dataset/NLP Dataset.xlsx")


REVIEW_COLUMN = "text"

# Stopwords
stop_words = set(stopwords.words("english"))

# Text preprocessing function
def clean_text(text):
    if pd.isna(text):
        return ""

    # 1. Convert to lowercase
    text = text.lower()

    # 2. Remove punctuation, numbers and special characters
    text = re.sub(r'[^a-z\s]', '', text)

    # 3. Remove stopwords
    words = text.split()
    words = [word for word in words if word not in stop_words]

    return " ".join(words)

# Create cleaned review column
df["Clean_Review"] = df[REVIEW_COLUMN].apply(clean_text)

# Save cleaned dataset
df.to_csv("dataset/cleaned_reviews.csv", index=False)

print("✅ Preprocessing completed successfully!")
print(df.head())