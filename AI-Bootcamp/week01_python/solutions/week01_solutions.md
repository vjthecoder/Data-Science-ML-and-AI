# Week 1 Solutions

Reference solutions for `../assignments/week01_assignments.md`. Try the assignments yourself
first.

---

## Solution 1 — Python Fundamentals

```python
order = {"order_id": 5001, "customer": "Asha", "items": ["Tea", "Mug", "Notebook"],
         "price_total": "899.00", "is_gift": True}

price_total = float(order["price_total"])
gst = round(price_total * 0.18, 2)
grand_total = round(price_total + gst, 2)

def format_order(order: dict) -> str:
    price = float(order["price_total"])
    gst = round(price * 0.18, 2)
    total = round(price + gst, 2)
    return (f"Order #{order['order_id']} for {order['customer']}: "
            f"{len(order['items'])} items, subtotal ₹{price:.2f}, "
            f"GST ₹{gst:.2f}, grand total ₹{total:.2f}")

print(format_order(order))
```

---

## Solution 2 — Control Flow

```python
temps = [12, 25, 38, 41, 18, 5, 29]
counts = {"Freezing": 0, "Cold": 0, "Mild": 0, "Hot": 0, "Extreme": 0}
categories = []

for t in temps:
    if t < 0:
        cat = "Freezing"
    elif t < 15:
        cat = "Cold"
    elif t < 28:
        cat = "Mild"
    elif t < 38:
        cat = "Hot"
    else:
        cat = "Extreme"
    categories.append(cat)
    counts[cat] += 1

print(counts)

# Longest streak of Hot/Extreme
longest = current = 0
for cat in categories:
    if cat in ("Hot", "Extreme"):
        current += 1
        longest = max(longest, current)
    else:
        current = 0
print("Longest hot streak:", longest)
```

---

## Solution 3 — Functions & OOP

```python
def restock_alert(current_qty: int, reorder_level: int) -> bool:
    return current_qty <= reorder_level


class Product:
    def __init__(self, name, current_qty, reorder_level, price):
        self.name = name
        self.current_qty = current_qty
        self.reorder_level = reorder_level
        self.price = price

    def inventory_value(self) -> float:
        return self.current_qty * self.price

    def needs_restock(self) -> bool:
        return restock_alert(self.current_qty, self.reorder_level)


class PerishableProduct(Product):
    def __init__(self, name, current_qty, reorder_level, price, expiry_date, today):
        super().__init__(name, current_qty, reorder_level, price)
        self.expiry_date = expiry_date
        self.today = today

    def inventory_value(self) -> float:
        if self.expiry_date < self.today:
            return 0.0
        return super().inventory_value()


p = Product("Pen", 5, 10, 20)
print(p.needs_restock(), p.inventory_value())

pp = PerishableProduct("Milk", 10, 5, 60, expiry_date="2024-01-01", today="2024-02-01")
print(pp.inventory_value())  # 0.0, expired
```

---

## Solution 4 — NumPy

```python
import numpy as np

rng = np.random.default_rng(7)
temps = rng.normal(loc=25, scale=5, size=100)

mean, median, std = temps.mean(), np.median(temps), temps.std()
print(mean, median, std, temps.min(), temps.max())

hot_days = (temps > 30).sum()
print("Days > 30:", hot_days)

standardized = (temps - mean) / std

hottest_5_idx = np.argsort(temps)[-5:]
print("Hottest 5 indices:", hottest_5_idx, "values:", temps[hottest_5_idx])
```

---

## Solution 5 — Pandas

```python
import pandas as pd

df = pd.read_csv("resources/datasets/customers.csv")

median_spend_by_plan = df.groupby("plan")["monthly_spend"].median()

top3_cities = df["city"].value_counts().head(3)

df["signup_date"] = pd.to_datetime(df["signup_date"])
df["signup_year"] = df["signup_date"].dt.year

inactive_by_plan = df[df["is_active"] == 0].groupby("plan").size()
inactive_free = df[(df["is_active"] == 0) & (df["plan"] == "Free")]
pct_inactive_free = len(inactive_free) / (df["is_active"] == 0).sum() * 100

print(median_spend_by_plan)
print(top3_cities)
print(inactive_by_plan)
print(f"{pct_inactive_free:.1f}% of inactive customers are on Free plan")
```

---

## Solution 6 — Visualization

```python
import pandas as pd, matplotlib.pyplot as plt, seaborn as sns

sales = pd.read_csv("resources/datasets/sales.csv")
sales["date"] = pd.to_datetime(sales["date"])

weekly = sales.set_index("date").resample("W")["revenue"].sum()
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(weekly.index, weekly.values, marker="o")
ax.set_title("Weekly Revenue"); ax.set_ylabel("Revenue (₹)")

fig2, ax2 = plt.subplots(figsize=(8, 4))
sns.barplot(x="region", y="revenue", hue="category", data=sales, estimator=sum, ax=ax2)
ax2.set_title("Revenue by Region and Category")

fig3, ax3 = plt.subplots(figsize=(6, 5))
sns.scatterplot(x="units", y="revenue", hue="category", data=sales, ax=ax3)
ax3.set_title("Units vs Revenue")
```

---

## Solution 7 — APIs & JSON

```python
import requests, json, pandas as pd

def fetch_posts(user_id):
    try:
        resp = requests.get(f"https://jsonplaceholder.typicode.com/posts?userId={user_id}", timeout=5)
        resp.raise_for_status()
        return resp.json()
    except Exception:
        return [{"id": 1, "title": "Mock title", "body": "Mock body"}]

posts = fetch_posts(1)
df = pd.DataFrame(posts)[["id", "title", "body"]]
df.to_json("posts.json", orient="records", indent=2)

def count_posts():
    return len(pd.read_json("posts.json"))

print(count_posts())
```

---

## Solution 8 — SQL Integration

```python
import sqlite3, pandas as pd

conn = sqlite3.connect(":memory:")
sales = pd.read_csv("resources/datasets/sales.csv")
sales.to_sql("sales", conn, index=False, if_exists="replace")

revenue_by_region = pd.read_sql(
    "SELECT region, SUM(revenue) AS total_revenue FROM sales GROUP BY region ORDER BY total_revenue DESC",
    conn,
)

top3_products = pd.read_sql(
    "SELECT product, SUM(units) AS total_units FROM sales GROUP BY product ORDER BY total_units DESC LIMIT 3",
    conn,
)

def sales_in_category(conn, category):
    return pd.read_sql("SELECT * FROM sales WHERE category = ?", conn, params=(category,))

best_month = pd.read_sql(
    """
    SELECT strftime('%m', date) AS month, SUM(revenue) AS total_revenue
    FROM sales GROUP BY month ORDER BY total_revenue DESC LIMIT 1
    """,
    conn,
)

print(revenue_by_region)
print(top3_products)
print(best_month)
```
