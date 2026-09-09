"""
Sales Data Analysis using Python
---------------------------------
Internship project - Python Developer Intern @ Codec Technologies
By: Pulkit Singh

Basically just going through a sales dataset to answer 3 questions:
  1. How are monthly sales trending?
  2. Which products are actually making the most money?
  3. Is any one region carrying most of the sales?

Run it with:
    python3 sales_analysis.py

It prints a summary to the console and drops 3 charts into output_charts/.
"""

import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUTPUT_DIR = "output_charts"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def load_data(path="sales_data.csv"):
    """Just reads the CSV and makes sure Date is parsed properly."""
    df = pd.read_csv(path, parse_dates=["Date"])
    return df


def clean_data(df):
    """Drop duplicates/blank rows, and add a Month column for grouping later."""
    df = df.drop_duplicates()
    df = df.dropna()
    df["Month"] = df["Date"].dt.to_period("M").astype(str)
    return df


def total_revenue(df):
    return round(df["TotalSale"].sum(), 2)


def monthly_trend(df):
    return df.groupby("Month")["TotalSale"].sum().round(2)


def top_products(df, n=5):
    return (
        df.groupby("Product")["TotalSale"]
        .sum()
        .sort_values(ascending=False)
        .head(n)
        .round(2)
    )


def region_wise_sales(df):
    return df.groupby("Region")["TotalSale"].sum().round(2)


def plot_monthly_trend(monthly):
    plt.figure(figsize=(8, 5))
    monthly.plot(kind="line", marker="o", color="#2E86AB")
    plt.title("Monthly Sales Trend")
    plt.xlabel("Month")
    plt.ylabel("Total Sales (INR)")
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/monthly_trend.png", dpi=150)
    plt.close()


def plot_top_products(top_n):
    plt.figure(figsize=(8, 5))
    top_n.sort_values().plot(kind="barh", color="#F18F01")
    plt.title("Top-Selling Products by Revenue")
    plt.xlabel("Total Sales (INR)")
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/top_products.png", dpi=150)
    plt.close()


def plot_region_sales(region_sales):
    plt.figure(figsize=(6, 6))
    plt.pie(region_sales, labels=region_sales.index, autopct="%1.1f%%",
            colors=["#2E86AB", "#F18F01", "#C73E1D", "#3B1F2B"])
    plt.title("Region-wise Sales Contribution")
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/region_sales.png", dpi=150)
    plt.close()


def main():
    df = load_data()
    df = clean_data(df)

    revenue = total_revenue(df)
    monthly = monthly_trend(df)
    top5 = top_products(df)
    region_sales = region_wise_sales(df)

    print("=" * 50)
    print("SALES DATA ANALYSIS REPORT")
    print("=" * 50)
    print(f"Total Records Analyzed : {len(df)}")
    print(f"Total Revenue          : Rs. {revenue:,.2f}")
    print("\nMonthly Sales Trend:\n", monthly)
    print("\nTop 5 Products by Revenue:\n", top5)
    print("\nRegion-wise Sales:\n", region_sales)

    plot_monthly_trend(monthly)
    plot_top_products(top5)
    plot_region_sales(region_sales)

    print(f"\nCharts saved in '{OUTPUT_DIR}/' folder.")


if __name__ == "__main__":
    main()
