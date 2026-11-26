"""
app.py — Internship Scam Checker
Flask backend combining a rule-based red-flag engine with a TF-IDF +
Logistic Regression classifier to assess whether an internship
email / message / WhatsApp text is likely genuine or a scam.

Run:
    python3 train_model.py   # once, to build model/scam_model.joblib
    python3 app.py
Then open http://127.0.0.1:5000
"""
import os
import re
import joblib
from flask import Flask, request, jsonify, render_template

from rules import analyze_text

app = Flask(__name__)

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model", "scam_model.joblib")
_model = None


def get_model():
    global _model
    if _model is None and os.path.exists(MODEL_PATH):
        _model = joblib.load(MODEL_PATH)
    return _model


def verdict_from_score(score):
    if score >= 65:
        return "HIGH RISK", "This message shows strong signs of an internship scam. Do not pay any money or share personal/bank details."
    if score >= 35:
        return "SUSPICIOUS", "Several warning signs are present. Verify independently before proceeding — see the checklist tips below."
    return "LIKELY GENUINE", "Few or no red flags detected. Still verify the company and offer through official channels before sharing sensitive information."


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json(force=True) or {}
    text = (data.get("text") or "").strip()
    channel = data.get("channel", "email")

    if not text:
        return jsonify({"error": "Please paste some message text to analyze."}), 400

    rule_result = analyze_text(text)
    rule_score = rule_result["rule_score"]

    ml_score = None
    model = get_model()
    if model is not None:
        try:
            proba = model.predict_proba([text])[0]
            classes = list(model.classes_)
            scam_idx = classes.index(1)
            ml_score = round(float(proba[scam_idx]) * 100, 1)
        except Exception:
            ml_score = None

    # Combined score: weight rules higher since they're explainable;
    # ML acts as a secondary cross-check, especially useful when the
    # text doesn't match any hand-written pattern.
    if ml_score is not None:
        combined = round(0.65 * rule_score + 0.35 * ml_score, 1)
    else:
        combined = rule_score

    label, advice = verdict_from_score(combined)

    return jsonify({
        "channel": channel,
        "rule_score": rule_score,
        "ml_score": ml_score,
        "combined_score": combined,
        "verdict": label,
        "advice": advice,
        "findings": rule_result["findings"],
        "positive_findings": rule_result["positive_findings"],
    })


@app.route("/call-checklist", methods=["GET"])
def call_checklist():
    """Static checklist for verifying a phone call in real time
    (audio isn't processed — this gives the caller structured prompts)."""
    checklist = [
        {"q": "Did they ask you to pay any fee, deposit, or 'training kit' cost?",
         "flag": "Any request for money is an automatic red flag — genuine internships never charge candidates."},
        {"q": "Did they ask for your bank account, card, Aadhaar, PAN, or an OTP over the call?",
         "flag": "No legitimate recruiter needs your OTP or full bank details on a phone call."},
        {"q": "Can they tell you the exact company name, and does the caller ID / callback number match the company's official listed number?",
         "flag": "Search the company's official website/HR contact yourself and compare — don't trust the number that called you."},
        {"q": "Are they pressuring you to decide or pay within minutes?",
         "flag": "Urgency ('offer expires in 30 minutes') is a manipulation tactic, not normal HR process."},
        {"q": "Did you apply to this company, or did the call come out of nowhere?",
         "flag": "Unsolicited 'you're selected' calls for jobs you never applied to are a common scam opener."},
        {"q": "Will they confirm the offer in writing on official company letterhead / email domain?",
         "flag": "Ask them to email the offer from an official company domain — refusal or a generic Gmail/Yahoo address is a red flag."},
        {"q": "Is the promised pay unusually high for minimal work (e.g. Rs 5000/day, no experience)?",
         "flag": "Unrealistic pay-for-effort ratios are a hallmark of task-based earning scams."},
    ]
    return jsonify(checklist)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(debug=debug, host="0.0.0.0", port=port)
