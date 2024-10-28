"""
Sales data analyzer program
"""

import random
import pandas as pd
import numpy as np
from faker import Faker

# Initialize Faker for generating random names and dates
fake = Faker()

# Define product categories
categories = ["Electronics", "Apparel", "Home Goods", "Books", "Toys"]

# Create dummy data
NUM_ENTRIES = 1000
data = {
    "Order_ID": np.arange(1, NUM_ENTRIES + 1),
    "Product_Category": [random.choice(categories) for _ in range(NUM_ENTRIES)],
    "Customer_Age": np.random.randint(18, 70, NUM_ENTRIES),
    "Order_Date": [fake.date_this_decade() for _ in range(NUM_ENTRIES)],
    "Sales_Amount": np.round(np.random.uniform(10, 500, NUM_ENTRIES), 2),
}

# Create DataFrame
df = pd.DataFrame(data)

# Save to CSV
CSV_FILE_PATH = "sales_data.csv"
df.to_csv(CSV_FILE_PATH, index=False)

# 1. Top-Selling Product Categories by Revenue
category_sales = (
    df.groupby("Product_Category")["Sales_Amount"].sum().sort_values(ascending=False)
)

# 2. Average Sales by Customer Age Group
# Define age groups
bins = [18, 30, 50, 70]
labels = ["18-30", "31-50", "51-70"]
df["Age_Group"] = pd.cut(df["Customer_Age"], bins=bins, labels=labels, right=False)
age_group_sales = df.groupby("Age_Group", observed=False)["Sales_Amount"].mean()

# 3. Monthly Sales Trend
# Convert 'Order_Date' to datetime
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df["Order_Month"] = df["Order_Date"].dt.to_period("M")
monthly_sales = df.groupby("Order_Month")["Sales_Amount"].sum()

# Display results
print(category_sales)

print(age_group_sales)

print(monthly_sales.head())
