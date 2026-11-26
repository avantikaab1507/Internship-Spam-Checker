"""
Generates data/internship_dataset.csv — a labeled synthetic dataset of
internship-related messages (emails / texts / WhatsApp style) used to
train the ML side of the scam checker.

label: 1 = scam, 0 = legitimate
"""
import csv
import random

random.seed(42)

companies = ["TCS", "Infosys", "Wipro", "Zoho", "Freshworks", "Accenture",
             "Capgemini", "Google", "Microsoft", "Amazon", "Flipkart",
             "Swiggy", "Byju's", "TVS Motors", "Ashok Leyland", "HCL"]

fake_companies = ["Global Career Solutions", "WorkFromHome Hub", "Elite Earners Pvt",
                   "QuickHire International", "TalentBridge Global", "NextGen Jobs Co",
                   "Digital Income Network", "SkillBoost Careers", "PrimeTask Recruiters",
                   "BrightFuture Placements"]

names = ["Arjun", "Priya", "Karthik", "Divya", "Suresh", "Meena", "Ramesh", "Anitha",
         "Vignesh", "Deepa", "Sundar", "Lakshmi", "Fulber", "Pranav", "Aarthi"]

legit_templates = [
    "Dear {name}, thank you for applying for the {role} internship at {company}. We would like to invite you for a technical interview on {date} via our official Google Meet link sent from careers@{domain}.com. Please bring your resume and a valid college ID.",
    "Hi {name}, this is HR from {company}. Your application for the Summer Internship Program has been shortlisted. The next round is a coding assessment hosted on our official portal at careers.{domain}.com. No payment is required at any stage.",
    "Hello {name}, congratulations! You have been selected for the {role} internship at {company}, starting {date}. Please find attached the offer letter on official letterhead. Kindly complete your onboarding on the employee portal using your college email ID.",
    "Dear {name}, we reviewed your resume for the {role} internship position. We would like to schedule a panel interview with our engineering team next week. Please confirm your availability by replying to this email from hr@{domain}.com.",
    "Hi {name}, thank you for your interest in {company}. Your profile matches our internship requirements. Please complete the assessment on HackerRank using the link below before {date}. Results will be communicated within 10 working days.",
    "Dear {name}, as discussed in your interview, we are pleased to offer you a {duration} internship at {company} in the {role} team. Stipend details and joining formalities are attached. Please reach out to your assigned mentor for any queries.",
    "Hello {name}, your application for {company}'s internship program has been received. Our recruitment team will contact you within two weeks if your profile is shortlisted for the next round.",
    "Hi {name}, this is a reminder that your final round interview for the {role} internship at {company} is scheduled for {date} at our office. Please carry two copies of your resume.",
]

scam_templates = [
    "Congratulations {name}! You have been selected for a WORK FROM HOME internship with {company}. Registration fee of Rs {amount} is required to activate your account. Pay immediately via UPI to confirm your seat, limited slots available!!!",
    "Hi {name}, we are offering a guaranteed internship + job placement with {company}. Just pay a refundable security deposit of Rs {amount} and send your Aadhaar card and bank details to proceed. Hurry, offer closes today.",
    "Dear candidate, {company} is hiring interns urgently. Earn Rs 5000/day working just 2 hours! No interview needed. Send Rs {amount} as registration fee to this number on WhatsApp to get your ID card and starter kit.",
    "Congratulations! Your resume has been selected by our AI system for {company} internship. To proceed, click this link and pay Rs {amount} processing fee within 30 minutes or your slot will be given to someone else.",
    "Hello {name}, this is from HR dept of {company}. We need your bank account number, IFSC code and Aadhaar number to process your internship stipend in advance. Reply urgently, this offer expires tonight.",
    "Hi, huge opportunity!! {company} internship program 2026, no experience needed, work from home, earn upto Rs 30000 monthly. Contact our HR on WhatsApp +91{phone} and pay Rs {amount} for the training kit.",
    "Dear {name}, you are shortlisted for {company} internship. Kindly install this app and pay Rs {amount} refundable token to unlock your task dashboard. 100% money back guaranteed after task completion.",
    "URGENT: Only 3 slots left for {company} summer internship! Pay registration fee of Rs {amount} now via Google Pay to this number to secure your seat. Certificate and stipend guaranteed, no interview required.",
    "Hi {name}, we loved your profile! Selected directly for {company} internship, skip the interview. Just complete KYC by sending Aadhaar, PAN card photo and pay Rs {amount} verification charge to our agent.",
    "Congratulations, your internship application is approved! To receive your offer letter and laptop kit from {company}, pay a one-time delivery charge of Rs {amount} to the courier account below.",
]

roles = ["Software Development", "Data Analyst", "Marketing", "HR", "Content Writing",
         "Web Development", "Graphic Design", "Digital Marketing", "Business Development"]
durations = ["2-month", "3-month", "6-week", "8-week", "summer"]
dates = ["15th September", "3rd October", "22nd August", "10th November", "5th December"]
amounts = ["499", "999", "1500", "2500", "3000", "4999"]


def make_domain(company):
    return company.lower().replace(" ", "").replace("'", "")


def gen(n_per_class=90):
    rows = []
    for _ in range(n_per_class):
        c = random.choice(companies)
        rows.append([
            random.choice(legit_templates).format(
                name=random.choice(names), role=random.choice(roles),
                company=c, domain=make_domain(c), date=random.choice(dates),
                duration=random.choice(durations)),
            0
        ])
    for _ in range(n_per_class):
        c = random.choice(fake_companies + companies)
        rows.append([
            random.choice(scam_templates).format(
                name=random.choice(names), company=c,
                amount=random.choice(amounts), phone=random.randint(10000000, 99999999)),
            1
        ])
    random.shuffle(rows)
    return rows


if __name__ == "__main__":
    rows = gen(110)
    with open("data/internship_dataset.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["text", "label"])
        w.writerows(rows)
    print(f"Wrote {len(rows)} rows to data/internship_dataset.csv")
