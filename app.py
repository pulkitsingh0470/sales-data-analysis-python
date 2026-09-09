"""
Sales Data Analysis - Interactive Dashboard
---------------------------------------------
Internship project - Python Developer Intern @ Codec Technologies
By: Pulkit Singh

Same analysis as sales_analysis.py, just wrapped in Streamlit so it can be
viewed and filtered live in the browser instead of only as static charts.

Run locally with:
    streamlit run app.py
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Sales Data Analysis", page_icon="📊", layout="wide")


@st.cache_data
def load_data():
    df = pd.read_csv("sales_data.csv", parse_dates=["Date"])
    df = df.drop_duplicates().dropna()
    df["Month"] = df["Date"].dt.to_period("M").astype(str)
    return df


df = load_data()

# ---------------- Header ----------------
st.title("📊 Sales Data Analysis Dashboard")
st.caption("Internship Project — Python Developer Intern, Codec Technologies")

st.markdown(
    "This dashboard analyzes transactional sales data using Pandas for "
    "aggregation and Matplotlib for visualization. Use the filters on the "
    "left to explore the data by region and product."
)

# ---------------- Sidebar filters ----------------
st.sidebar.header("Filters")

regions = sorted(df["Region"].unique())
selected_regions = st.sidebar.multiselect("Region", regions, default=regions)

products = sorted(df["Product"].unique())
selected_products = st.sidebar.multiselect("Product", products, default=products)

min_date, max_date = df["Date"].min(), df["Date"].max()
date_range = st.sidebar.date_input(
    "Date range", value=(min_date, max_date), min_value=min_date, max_value=max_date
)

# Apply filters
filtered = df[
    df["Region"].isin(selected_regions)
    & df["Product"].isin(selected_products)
]
if len(date_range) == 2:
    start, end = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
    filtered = filtered[(filtered["Date"] >= start) & (filtered["Date"] <= end)]

if filtered.empty:
    st.warning("No data matches the selected filters. Try widening your selection.")
    st.stop()

# ---------------- KPI row ----------------
total_revenue = filtered["TotalSale"].sum()
total_orders = len(filtered)
avg_order_value = total_revenue / total_orders if total_orders else 0

col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"Rs. {total_revenue:,.0f}")
col2.metric("Total Orders", f"{total_orders:,}")
col3.metric("Avg. Order Value", f"Rs. {avg_order_value:,.0f}")

st.divider()

# ---------------- Charts ----------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("Monthly Sales Trend")
    monthly = filtered.groupby("Month")["TotalSale"].sum().round(2)
    fig, ax = plt.subplots(figsize=(6, 4))
    monthly.plot(kind="line", marker="o", color="#2E86AB", ax=ax)
    ax.set_xlabel("Month")
    ax.set_ylabel("Total Sales (INR)")
    st.pyplot(fig)

with col2:
    st.subheader("Top-Selling Products")
    top_products = (
        filtered.groupby("Product")["TotalSale"].sum().sort_values(ascending=False).head(5).round(2)
    )
    fig, ax = plt.subplots(figsize=(6, 4))
    top_products.sort_values().plot(kind="barh", color="#F18F01", ax=ax)
    ax.set_xlabel("Total Sales (INR)")
    st.pyplot(fig)

st.subheader("Region-wise Sales Distribution")
region_sales = filtered.groupby("Region")["TotalSale"].sum().round(2)
fig, ax = plt.subplots(figsize=(5, 5))
ax.pie(region_sales, labels=region_sales.index, autopct="%1.1f%%",
       colors=["#2E86AB", "#F18F01", "#C73E1D", "#3B1F2B"])
st.pyplot(fig)

# ---------------- Raw data ----------------
with st.expander("View filtered raw data"):
    st.dataframe(filtered.sort_values("Date"), use_container_width=True)

st.divider()
st.caption("Built with Python, Pandas, Matplotlib & Streamlit.")
