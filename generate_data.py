# Run this only if you want to regenerate sales_data.csv
import csv, random
from datetime import date, timedelta
random.seed(42)
products=["Wireless Mouse","Mechanical Keyboard","USB-C Hub","Laptop Stand","Webcam HD","Bluetooth Speaker","Power Bank","Monitor Arm"]
regions=["North","South","East","West"]
prices={"Wireless Mouse":799,"Mechanical Keyboard":2499,"USB-C Hub":1299,"Laptop Stand":999,"Webcam HD":1799,"Bluetooth Speaker":1599,"Power Bank":1199,"Monitor Arm":2199}
rows=[]; d=date(2026,1,1); oid=1
while d<=date(2026,6,30):
    for _ in range(random.randint(3,6)):
        p=random.choice(products); r=random.choice(regions); q=random.randint(1,12); price=prices[p]
        rows.append([oid,d.isoformat(),p,r,q,price,round(q*price*random.uniform(.95,1.05),2)]); oid+=1
    d+=timedelta(days=1)
with open("sales_data.csv","w",newline="",encoding="utf-8") as f:
    w=csv.writer(f); w.writerow(["OrderID","Date","Product","Region","Quantity","UnitPrice","TotalSale"]); w.writerows(rows)
print("Generated",len(rows),"rows")
