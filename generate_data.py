"""
generate_data.py
Creates a synthetic sales dataset (sales_data.csv) for the internship project.
Data is randomly generated -> original, no plagiarism concerns.
"""
import csv
import random
from datetime import date, timedelta

random.seed(42)

products = ["Wireless Mouse", "Mechanical Keyboard", "USB-C Hub", "Laptop Stand",
            "Webcam HD", "Bluetooth Speaker", "Power Bank", "Monitor Arm"]
regions = ["North", "South", "East", "West"]

start_date = date(2026, 1, 1)
rows = []
current = start_date
row_id = 1

while current <= date(2026, 6, 30):
    # 3-6 random transactions per day
    for _ in range(random.randint(3, 6)):
        product = random.choice(products)
        region = random.choice(regions)
        quantity = random.randint(1, 12)
        base_price = {
            "Wireless Mouse": 799, "Mechanical Keyboard": 2499, "USB-C Hub": 1299,
            "Laptop Stand": 999, "Webcam HD": 1799, "Bluetooth Speaker": 1599,
            "Power Bank": 1199, "Monitor Arm": 2199
        }[product]
        price = base_price
        total = round(quantity * price * random.uniform(0.95, 1.05), 2)
        rows.append([row_id, current.isoformat(), product, region, quantity, price, total])
        row_id += 1
    current += timedelta(days=1)

with open("sales_data.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["OrderID", "Date", "Product", "Region", "Quantity", "UnitPrice", "TotalSale"])
    writer.writerows(rows)

print(f"Generated {len(rows)} rows -> sales_data.csv")
