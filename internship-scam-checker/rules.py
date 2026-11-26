"""
rules.py — Rule-based red-flag detector for internship scam messages.

Each rule is a (name, category, severity, pattern, explanation) tuple.
severity is 1 (minor) to 5 (severe). The engine scans the input text,
finds every matching span, and returns structured findings that the
frontend uses to highlight the exact phrases inline.
"""
import re

# A rule = id, category, severity (1-5), compiled regex, human explanation
RULES = [
    dict(
        id="fee_request",
        category="Money Request",
        severity=5,
        pattern=r"\b(registration fee|processing fee|security deposit|refundable (token|deposit)|training kit|verification charge|delivery charge|pay\s*(rs\.?|₹|inr)?\s*\d)",
        why="Legitimate employers never ask candidates to pay money — for registration, training kits, deposits, or 'processing' — at any stage of hiring."
    ),
    dict(
        id="bank_details",
        category="Sensitive Info Request",
        severity=5,
        pattern=r"\b(bank account number|ifsc code|aadhaar|aadhar|pan card|otp|debit card|credit card pin|upi pin)\b",
        why="Real recruiters don't need your bank account, Aadhaar/PAN scans, or OTP before you've even signed an offer letter. This is a data-harvesting or fraud request."
    ),
    dict(
        id="urgency",
        category="Pressure Tactic",
        severity=4,
        pattern=r"\b(urgent(ly)?|hurry|act now|limited slots?|only \d+ slots?|expires? (today|tonight|soon)|within \d+ minutes|offer closes|immediately)\b",
        why="Manufactured urgency ('only 3 slots left', 'pay in 30 minutes') is a classic pressure tactic to stop you from thinking it through or checking with anyone."
    ),
    dict(
        id="no_interview",
        category="Suspicious Process",
        severity=4,
        pattern=r"\b(no interview (needed|required)|skip the interview|selected directly|selected by our ai system|no experience needed)\b",
        why="Genuine internships almost always involve some screening (interview, test, or resume review). 'No interview, guaranteed selection' is a major red flag."
    ),
    dict(
        id="unrealistic_pay",
        category="Unrealistic Offer",
        severity=3,
        pattern=r"\b(earn (upto |up to )?rs\.?\s*\d{3,}\s*/?\s*(day|daily)|earn upto rs\.?\s*\d{4,}|just \d+ hours?.{0,15}(earn|day))",
        why="Promises of large daily earnings for 1-2 hours of unskilled work are a hallmark of pyramid/task-scam schemes, not real internships."
    ),
    dict(
        id="whatsapp_only",
        category="Unofficial Channel",
        severity=3,
        pattern=r"\b(contact.{0,15}(hr|us).{0,10}(on |via )?whatsapp|whatsapp (this )?number|reply on whatsapp)\b",
        why="Real HR communication happens over official email or a company career portal — not exclusively via a personal WhatsApp number."
    ),
    dict(
        id="generic_greeting",
        category="Impersonal Contact",
        severity=1,
        pattern=r"^(hi|hello|dear) (candidate|applicant|sir\/madam|there)\b",
        why="A message that doesn't address you by name suggests a mass-blast to many people rather than a genuine, individual response to your application."
    ),
    dict(
        id="grammar_shout",
        category="Tone / Grammar",
        severity=2,
        pattern=r"(!{2,}|CONGRATULATIONS|URGENT:|HUGE OPPORTUNITY)",
        why="Excessive punctuation, all-caps 'URGENT' banners, and hype language ('huge opportunity!!') are typical of mass scam blasts, not professional HR writing."
    ),
    dict(
        id="money_back_guarantee",
        category="Unrealistic Offer",
        severity=3,
        pattern=r"\b(100% money back|guaranteed (stipend|job|placement|selection)|money back guaranteed)\b",
        why="'Guaranteed' outcomes and money-back promises are sales tactics used to make a paid scheme sound risk-free — real internships don't need to 'guarantee' anything."
    ),
    dict(
        id="install_app",
        category="Suspicious Process",
        severity=3,
        pattern=r"\b(install this app|download (our|the) app|click this link|unlock your (task )?dashboard)\b",
        why="Being told to install an unfamiliar app or click a link before any formal process is a common way to deliver malware or lock you into a fake task platform."
    ),
]

_COMPILED = [(r, re.compile(r["pattern"], re.IGNORECASE | re.MULTILINE)) for r in RULES]

# Signals that reduce risk when present (legitimate-process indicators)
POSITIVE_SIGNALS = [
    dict(id="official_domain_mail", pattern=r"@[\w.-]+\.(com|in|co\.in|org)\b(?!.*(gmail|yahoo|outlook|hotmail))",
         why="Message references a company-domain email address rather than a generic personal one."),
    dict(id="no_payment_stated", pattern=r"\bno payment (is )?required\b",
         why="Message explicitly states no payment is required — a good sign, though scammers can also fake this line, so still verify independently."),
    dict(id="named_recipient", pattern=r"^(dear|hi|hello) [A-Z][a-z]+,",
         why="Message addresses you by name rather than a generic greeting."),
]
_POS_COMPILED = [(r, re.compile(r["pattern"], re.MULTILINE)) for r in POSITIVE_SIGNALS]


def analyze_text(text: str):
    """Scan text for red-flag and positive-signal matches.

    Returns dict with: findings (list), positive_findings (list), rule_score (0-100)
    """
    findings = []
    for rule, pattern in _COMPILED:
        for m in pattern.finditer(text):
            findings.append({
                "id": rule["id"],
                "category": rule["category"],
                "severity": rule["severity"],
                "why": rule["why"],
                "match": m.group(0),
                "start": m.start(),
                "end": m.end(),
            })

    positive_findings = []
    for rule, pattern in _POS_COMPILED:
        m = pattern.search(text)
        if m:
            positive_findings.append({
                "id": rule["id"],
                "why": rule["why"],
                "match": m.group(0),
            })

    # Deduplicate overlapping matches (keep highest severity per overlapping span)
    findings.sort(key=lambda f: (f["start"], -f["severity"]))
    deduped = []
    last_end = -1
    for f in findings:
        if f["start"] >= last_end:
            deduped.append(f)
            last_end = f["end"]
    findings = deduped

    # Score: sum severities (capped), minus small credit for positive signals
    raw = sum(f["severity"] for f in findings)
    raw -= len(positive_findings) * 1.5
    rule_score = max(0, min(100, round((raw / 14) * 100)))  # 14 ~= a heavily flagged message

    return {
        "findings": findings,
        "positive_findings": positive_findings,
        "rule_score": rule_score,
    }
