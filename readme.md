# Workforce Burnout & Retention Tracker

Built this to answer a question I kept thinking about — can you tell which employees are likely to quit *before* they actually do? Turns out, yes, with the right business logic and a proactive scoring model.

Uses the IBM HR Analytics dataset (1,470 employees). The output is no longer a static file, but a live, interactive web dashboard built with Streamlit that an HR team can actively use to retain talent.

---

## The idea

Most attrition analysis is retrospective — you look at who left and why after the fact. I wanted to flip that. So instead of just doing Exploratory Data Analysis (EDA), I built a weighted heuristic risk score for each active employee and bucketed them into Low / Medium / High flight-risk tiers.

The score pulls from 7 features that show up consistently as attrition drivers. I moved beyond just standard satisfaction surveys and engineered new features like **Commute Fatigue** and **Financial Stagnation**. Each gets a weight based on how strongly it correlates with an employee's decision to leave.

Then I validated it — if the model is working, High tier employees should have a noticeably higher actual attrition rate than Low tier ones. The model successfully confirmed this logic, showing a massive spike in actual exits within the 'High Risk' tier compared to the 'Low Risk' tier.

---

## Numbers that stood out

- Overall historical attrition rate: **16.12%** (237 exits out of 1,470)
- Sales department consistently shows the highest attrition rate (~20%)
- **Over 200 currently active employees** are flagged as 'High Risk'
- Overtime and Commute Distance combined are incredibly strong burnout signals

---

## Smart Risk Score Breakdown

| Feature | Weight | Why |
|---|---|---|
| Job Satisfaction (inverted) | ×3 | Consistently the strongest predictor |
| Overtime | ×3 | Burnout — people doing OT leave faster |
| Commute Fatigue (>15km) | ×2 | Long daily travel directly impacts retention |
| Salary Stagnation (Hike <12%) | ×2 | Financial dissatisfaction drives immediate exits |
| Tenure < 3 years | ×2 | Early attrition is a highly common trend |
| Work-Life Balance (inverted) | ×2 | Gradual but meaningful signal |
| No promotion in 5+ years | ×2 | Career stagnation drives exits |

Tiers: **Low = 0–7 | Medium = 8–14 | High = 15+**

---

## Interactive Dashboard

The script powers a live web application featuring:

- **Executive Summary** — Top KPIs and active flight-risk staff count.
- **Risk Validation Charts** — Visual proof comparing predicted risk tiers against actual historical attrition.
- **HR Action Table** — A filtered, sortable list of active employees currently in the "High Risk" tier, providing HR with exactly who to talk to today.

---

## Stack

Python · Streamlit (Web Framework) · Pandas · NumPy · Matplotlib · Seaborn

---

## How to run locally

```bash
# Clone the repository
git clone https://github.com/yourusername/workforce-retention-tracker.git
cd workforce-retention-tracker

# Install required dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py
```
*(Note: If you face execution policy errors on Windows, use `python -m streamlit run app.py`)*

---

## Files

```text
├── app.py               # Main Streamlit application and scoring logic
├── requirements.txt     # Python dependencies
└── README.md
```

---

## What I'd do next

- Connect the app to a live SQL database instead of a static CSV for real-time HR syncing.
- Add an 'Estimated Replacement Cost' metric to quantify the financial impact of losing high-risk staff.