# Week 1 Assignments

Complete each assignment in a new Marimo notebook (or `.py` script) inside this folder,
named `assignment<N>_<your_name>.py`. Reference solutions are in `../solutions/`.

---

## Assignment 1 — Python Fundamentals (Variables & Types)

A subscription box company stores each order as a dictionary:
```python
order = {"order_id": 5001, "customer": "Asha", "items": ["Tea", "Mug", "Notebook"],
         "price_total": "899.00", "is_gift": True}
```
1. Convert `price_total` to a `float`.
2. Compute `gst = price_total * 0.18` and `grand_total = price_total + gst`.
3. Print a formatted summary string using an f-string.
4. **Bonus:** Write a function `format_order(order: dict) -> str` that returns the summary
   string, with type hints.

---

## Assignment 2 — Control Flow

Given a list of daily temperatures in Celsius:
```python
temps = [12, 25, 38, 41, 18, 5, 29]
```
1. Loop through and classify each as "Freezing" (<0), "Cold" (<15), "Mild" (<28), "Hot" (<38),
   or "Extreme" (>=38).
2. Count how many days fall into each category.
3. Find the longest streak of consecutive "Hot" or "Extreme" days using a `while` or `for` loop.

---

## Assignment 3 — Functions & OOP

Build a small inventory management system:
1. Write a function `restock_alert(current_qty, reorder_level) -> bool`.
2. Create a class `Product` with attributes `name`, `current_qty`, `reorder_level`, `price`.
3. Add a method `inventory_value()` returning `current_qty * price`.
4. Add a method `needs_restock()` using the function from step 1.
5. Create a subclass `PerishableProduct(Product)` with an extra `expiry_date` attribute and
   an overridden method `inventory_value()` that returns 0 if expired (you can hardcode
   "today" as a string for comparison).

---

## Assignment 4 — NumPy

Using `np.random.default_rng(7)`, generate an array of 100 simulated daily temperatures
(`rng.normal(loc=25, scale=5, size=100)`).
1. Compute mean, median (`np.median`), std, min, max.
2. Find the number of days above 30°C.
3. Standardize the array: `(x - mean) / std`.
4. Find the indices of the 5 hottest days (`np.argsort`).

---

## Assignment 5 — Pandas

Using `resources/datasets/customers.csv`:
1. Find the median `monthly_spend` for each `plan`.
2. Find the top 3 cities by number of customers.
3. Create a column `signup_year` extracted from `signup_date`.
4. Find the inactive customer count per plan, and the percentage of inactive customers
   that are on the "Free" plan.

---

## Assignment 6 — Visualization

Using `resources/datasets/sales.csv`:
1. Create a line chart of weekly revenue (resample by week).
2. Create a grouped bar chart: revenue by region, split by category (hint:
   `sns.barplot(x="region", y="revenue", hue="category", ...)`).
3. Create a scatter plot of `units` vs `revenue`, colored by `category`.
4. Add appropriate titles, axis labels, and a legend to all charts.

---

## Assignment 7 — APIs & JSON

1. Write a function `fetch_posts(user_id)` that calls
   `https://jsonplaceholder.typicode.com/posts?userId={user_id}` and returns the JSON list
   (with a mock fallback if offline).
2. Parse the result into a Pandas DataFrame with columns `id`, `title`, `body`.
3. Save the DataFrame to `posts.json` using `df.to_json(orient="records", indent=2)`.
4. Write a function that reads `posts.json` back and returns the number of posts.

---

## Assignment 8 — SQL Integration

Using `resources/datasets/sales.csv` loaded into an in-memory SQLite database:
1. Write a SQL query for total revenue per `region`, ordered descending.
2. Write a SQL query for the top 3 best-selling `product`s by total `units`.
3. Write a parameterized function `sales_in_category(conn, category)` returning all rows
   for a given category.
4. **Bonus:** Write a query that returns the month (from `date`) with the highest total
   revenue, using SQLite date functions (`strftime('%m', date)`).
