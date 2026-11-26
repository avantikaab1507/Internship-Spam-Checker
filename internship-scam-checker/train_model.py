"""
train_model.py — trains a TF-IDF + Logistic Regression classifier on
data/internship_dataset.csv and saves it to model/scam_model.joblib.

Run this once before starting the app:
    python3 train_model.py
"""
import csv
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.pipeline import Pipeline

DATA_PATH = "data/internship_dataset.csv"
MODEL_PATH = "model/scam_model.joblib"


def load_data(path):
    texts, labels = [], []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            texts.append(row["text"])
            labels.append(int(row["label"]))
    return texts, labels


def main():
    texts, labels = load_data(DATA_PATH)
    X_train, X_test, y_train, y_test = train_test_split(
        texts, labels, test_size=0.2, random_state=42, stratify=labels
    )

    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=1, stop_words="english")),
        ("clf", LogisticRegression(max_iter=1000, C=2.0)),
    ])

    pipeline.fit(X_train, y_train)
    preds = pipeline.predict(X_test)

    print("Accuracy:", accuracy_score(y_test, preds))
    print(classification_report(y_test, preds, target_names=["legit", "scam"]))

    joblib.dump(pipeline, MODEL_PATH)
    print(f"Saved model to {MODEL_PATH}")


if __name__ == "__main__":
    main()
