# Internship Scam Checker
### AI-Powered Internship Offer Verification and Risk Assessment System

## 1. Project Overview

Internship Scam Checker is an AI-assisted application designed to help students identify potentially fraudulent internship opportunities.

Students frequently encounter fake internship offers through emails, SMS messages, WhatsApp messages and phone calls. These offers may involve registration fees, security deposits, requests for sensitive personal information and unrealistic stipend promises.

This project combines rule-based detection and machine learning to analyse internship-related messages, identify suspicious indicators and provide an understandable risk assessment.

**Competition:** PromptWars – AI Prompt Challenge  
**Target Users:** Students and fresh graduates  
**Application Type:** AI-assisted web application

## 2. Problem Statement

Students searching for internships may struggle to distinguish genuine opportunities from fraudulent recruitment messages.

Scammers often use attractive stipend offers, false selection notifications, urgent payment requests and misleading recruitment procedures to deceive applicants.

There is a need for an accessible tool that can examine internship-related messages, identify warning signs and help students make informed decisions.

## 3. Proposed Solution

Internship Scam Checker provides an interface where users can submit internship-related messages for analysis.

The application combines two detection mechanisms:

- Rule-Based Detection: Identifies predefined scam indicators using regular expressions and assigns severity levels.
- Machine Learning Classification: Uses a TF-IDF vectoriser and Logistic Regression classifier to estimate the likelihood of a scam.

The two results are combined to generate an overall risk score and corresponding assessment.

## 4. Key Features

- Internship message analysis.
- Rule-based detection of suspicious phrases.
- Machine learning-based scam classification.
- Combined risk scoring.
- Identification of suspicious indicators.
- Explanations for detected warning signs.
- Positive indicator detection.
- Interactive phone-call verification checklist.
- Recommendations for safer internship verification.

## 5. Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Backend | Flask |
| Machine Learning | Scikit-learn |
| Text Vectorisation | TF-IDF |
| Classification Algorithm | Logistic Regression |
| Model Storage | Joblib |
| Frontend | HTML, CSS, JavaScript |
| Dataset | CSV |
| Deployment Configuration | Render YAML |

## 6. System Architecture

The application follows this processing workflow:

1. User enters an internship-related message.
2. Flask receives the submitted message.
3. The rule-based engine scans for suspicious indicators.
4. The machine learning model estimates scam probability.
5. The two scores are combined.
6. The application generates a risk category.
7. Detected findings and explanations are returned to the user.

### Risk Assessment Formula

When both detection mechanisms are available:

Combined Risk Score = (0.65 × Rule Score) + (0.35 × ML Score)

The resulting score is classified into three categories:

| Score | Assessment |
|---|---|
| Below 35 | Likely Genuine |
| 35–64 | Suspicious |
| 65–100 | High Risk |

The classification is an indicator for decision support, not a guarantee of legitimacy or fraud.

## 7. Rule-Based Detection

The application checks for indicators such as:

- Registration and processing fee requests.
- Security deposits and training kit charges.
- Requests for Aadhaar, PAN, bank details and OTPs.
- Urgent payment demands.
- Unrealistic stipend promises.
- Suspicious WhatsApp-only recruitment.
- Guaranteed selection without interviews.
- Misleading money-back promises.
- Suspicious application and installation instructions.

Each detected indicator has a severity level and an explanation.

## 8. Machine Learning Approach

The project uses a TF-IDF vectorisation approach to convert message text into numerical features.

A Logistic Regression classifier is trained to distinguish between legitimate and scam-related internship messages.

The project includes a synthetic labelled dataset for model training and evaluation.

The machine learning prediction acts as a secondary assessment alongside the explainable rule-based detection mechanism.

## 9. Phone Call Verification Checklist

The application also provides an interactive checklist for users who receive internship-related phone calls.

It helps users consider:

- Whether the caller requested money.
- Whether sensitive information was requested.
- Whether the company and contact number can be independently verified.
- Whether the caller created unnecessary urgency.
- Whether the user actually applied for the opportunity.
- Whether an official written offer is available.
- Whether the promised compensation is realistic.

The current checklist is manual; automatic audio transcription and call analysis are not implemented.

## 10. Project Structure

```text
internship-scam-checker/
│
├── app.py
├── rules.py
├── train_model.py
├── requirements.txt
├── render.yaml
│
├── data/
│   ├── generate_dataset.py
│   └── internship_dataset.csv
│
├── model/
│   └── scam_model.joblib
│
├── templates/
│   └── index.html
│
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── script.js
```

## 11. Installation and Execution

### Prerequisites

- Python 3.11 or compatible version
- Git
- pip

### Clone the repository

```bash
git clone https://github.com/FulberRenika/internship-scam-check.git
cd internship-scam-check/internship-scam-checker
```

### Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the application

```bash
python app.py
```

Open the following address in your browser:

```text
http://127.0.0.1:5000
```

## 12. Evaluation and Testing Considerations

The application can be evaluated using different internship message scenarios:

- Legitimate internship communication.
- Messages containing registration fee requests.
- Messages requesting sensitive personal information.
- Unsolicited internship selection messages.
- Messages containing unrealistic stipend promises.
- Suspicious WhatsApp recruitment messages.

The application returns the detected indicators, risk assessment and explanations for the submitted text.

## 13. Assumptions and Limitations

- The model is trained using a synthetic labelled dataset.
- Detection depends on the supplied message and predefined indicators.
- A low risk score does not establish that an internship is genuine.
- A high risk score does not independently prove criminal activity.
- Phone calls are assessed through a manual checklist rather than automatic audio processing.
- The application does not currently perform independent company registration or website verification.
- Users should independently verify internship opportunities through official company websites and verified recruitment contacts.

## 14. Future Enhancements

- Context-aware assessment using additional user-provided information.
- Company and website verification.
- URL reputation analysis.
- Speech-to-text integration for phone calls.
- Multilingual scam message detection.
- User feedback and model improvement.
- Enhanced explainable AI recommendations.

## 15. Disclaimer

Internship Scam Checker is an educational decision-support application. Its predictions should not be treated as definitive proof that an internship opportunity is genuine or fraudulent.

Users should independently verify organisations and avoid sharing sensitive information or making payments without proper verification.

---

**Developed by:** Fulber Renika C R  
**GitHub:** https://github.com/FulberRenika
