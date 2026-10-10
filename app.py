import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="Retention Tracker", layout="wide", page_icon="📊")

st.title("🚀 Workforce Burnout & Retention Tracker")
st.markdown("Yeh dashboard smart HR rules (Commute, Salary Hike, Satisfaction, Overtime) ke basis pe active employees ka flight-risk calculate karta hai.")
st.markdown("---")

# --- 2. DATA LOAD & LOGIC ---
@st.cache_data
def load_data():
    # Live URL se IBM HR dataset download kar rahe hain
    url = "https://raw.githubusercontent.com/IBM/employee-attrition-aif360/master/data/emp_attrition.csv"
    df = pd.read_csv(url)
    
    # Purane Metrics (Inverted taaki high score = high risk)
    df["Satisfaction_Risk"] = 4 - df["JobSatisfaction"]
    df["WLB_Risk"] = 4 - df["WorkLifeBalance"]
    df["Overtime_Risk"] = (df["OverTime"] == "Yes").astype(int)
    df["Tenure_Risk"] = np.where(df["YearsAtCompany"] < 3, 2, 0)
    df["Promotion_Risk"] = np.where(df["YearsSinceLastPromotion"] >= 5, 2, 0)
    
    # NAYE Metrics (Recruiter ko impress karne wale)
    df["Commute_Risk"] = np.where(df["DistanceFromHome"] >= 15, 2, 0)
    df["SalaryHike_Risk"] = np.where(df["PercentSalaryHike"] < 12, 2, 0)
    
    # Smart Score Calculation (Total max score = 16)
    df["Smart_Risk_Score"] = (
        df["Satisfaction_Risk"] * 3 +
        df["Overtime_Risk"] * 3 +
        df["Tenure_Risk"] * 2 +
        df["WLB_Risk"] * 2 +
        df["Promotion_Risk"] * 2 +
        df["Commute_Risk"] * 2 +
        df["SalaryHike_Risk"] * 2
    )
    
    # Risk Tiers mein divide karna
    df["Risk_Tier"] = pd.cut(
        df["Smart_Risk_Score"],
        bins=[0, 7, 14, 100],
        labels=["Low", "Medium", "High"],
        include_lowest=True
    )
    
    # Attrition ko Yes/No se 1/0 mein convert kiya for calculations
    df["Attrition_Flag"] = (df["Attrition"] == "Yes").astype(int)
    return df

# Data fetch function call
df = load_data()

# --- 3. SIDEBAR FILTERS ---
st.sidebar.header("🔍 Filter Options")
dept_filter = st.sidebar.selectbox("Select Department", ["All"] + list(df["Department"].unique()))

if dept_filter != "All":
    df = df[df["Department"] == dept_filter]

# --- 4. TOP KPIs ---
st.subheader("📊 Executive Summary")
col1, col2, col3, col4 = st.columns(4)

total_emp = len(df)
total_left = df["Attrition_Flag"].sum()
attrition_rate = (total_left / total_emp) * 100 if total_emp > 0 else 0

# Wo log jo abhi company mein hain (Attrition==0) par high risk par hain
high_risk_active = df[(df["Risk_Tier"] == "High") & (df["Attrition_Flag"] == 0)]

col1.metric("Total Employees", total_emp)
col2.metric("Total Exits (Historical)", total_left)
col3.metric("Overall Attrition Rate", f"{round(attrition_rate, 2)}%")
col4.metric("🚨 High Risk (Active Staff)", len(high_risk_active))

st.markdown("---")

# --- 5. CHARTS & VISUALIZATIONS ---
st.subheader("📈 Risk Analysis & Validation")
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.markdown("**Attrition Rate by Department**")
    dept_summary = df.groupby("Department").agg(
        Total=("EmployeeNumber", "count"), Left=("Attrition_Flag", "sum")
    ).reset_index()
    dept_summary["Rate (%)"] = (dept_summary["Left"] / dept_summary["Total"]) * 100
    
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(x="Department", y="Rate (%)", data=dept_summary, palette="Reds_d", ax=ax)
    plt.xticks(rotation=15)
    st.pyplot(fig)

with chart_col2:
    st.markdown("**Risk Model Validation (Actual vs Predicted)**")
    # Dekhne ke liye ki humara model sahi chal raha hai ya nahi
    tier_summary = df.groupby("Risk_Tier", observed=True).agg(
        Total=("EmployeeNumber", "count"), Left=("Attrition_Flag", "sum")
    ).reset_index()
    tier_summary["Actual Attrition (%)"] = (tier_summary["Left"] / tier_summary["Total"]) * 100
    
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    sns.barplot(x="Risk_Tier", y="Actual Attrition (%)", data=tier_summary, palette="coolwarm", ax=ax2)
    st.pyplot(fig2)

st.markdown("---")

# --- 6. ACTIONABLE DATA TABLE ---
st.subheader("🚨 High Risk Employees (HR Action Required)")
st.write("Ye un employees ki list hai jo company chhod sakte hain based on our scoring model.")

# Kaunse columns dashboard par dikhane hain
display_cols = [
    "EmployeeNumber", "Department", "JobRole", "Smart_Risk_Score", 
    "OverTime", "DistanceFromHome", "PercentSalaryHike", "JobSatisfaction"
]

st.dataframe(
    high_risk_active[display_cols].sort_values("Smart_Risk_Score", ascending=False), 
    use_container_width=True,
    hide_index=True
)