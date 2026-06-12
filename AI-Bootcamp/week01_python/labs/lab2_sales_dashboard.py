import marimo

__generated_with = "0.9.0"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    return mo, pd, plt, sns


@app.cell
def __(mo):
    mo.md(
        r"""
        # Lab 2: Sales Dashboard

        **Goal:** Build a multi-chart sales dashboard from `resources/datasets/sales.csv`.

        ## Tasks
        1. Load data, parse dates.
        2. KPI cards: total revenue, total units, average order value.
        3. Chart 1: Monthly revenue trend (line).
        4. Chart 2: Revenue by region (bar).
        5. Chart 3: Revenue share by category (pie or bar).
        6. Chart 4: Revenue heatmap (region x category).
        """
    )
    return


@app.cell
def __(pd):
    sales = pd.read_csv("../../resources/datasets/sales.csv")
    sales["date"] = pd.to_datetime(sales["date"])
    sales.head()
    return (sales,)


@app.cell
def __(sales):
    # KPIs
    total_revenue = sales["revenue"].sum()
    total_units = sales["units"].sum()
    avg_order_value = sales["revenue"].mean()

    print(f"Total Revenue: ₹{total_revenue:,.2f}")
    print(f"Total Units: {total_units:,}")
    print(f"Avg Order Value: ₹{avg_order_value:,.2f}")
    return avg_order_value, total_revenue, total_units


@app.cell
def __(plt, sales):
    monthly = sales.set_index("date").resample("M")["revenue"].sum()
    fig1, ax1 = plt.subplots(figsize=(7, 4))
    ax1.plot(monthly.index, monthly.values, marker="o", color="steelblue")
    ax1.set_title("Monthly Revenue Trend")
    ax1.set_ylabel("Revenue (₹)")
    fig1.autofmt_xdate()
    fig1
    return ax1, fig1, monthly


@app.cell
def __(plt, sales, sns):
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    region_rev = sales.groupby("region")["revenue"].sum().sort_values(ascending=False)
    sns.barplot(x=region_rev.index, y=region_rev.values, ax=ax2, palette="viridis")
    ax2.set_title("Revenue by Region")
    fig2
    return ax2, fig2, region_rev


@app.cell
def __(plt, sales):
    fig3, ax3 = plt.subplots(figsize=(5, 5))
    cat_rev = sales.groupby("category")["revenue"].sum()
    ax3.pie(cat_rev.values, labels=cat_rev.index, autopct="%1.1f%%")
    ax3.set_title("Revenue Share by Category")
    fig3
    return ax3, cat_rev, fig3


@app.cell
def __(pd, plt, sales, sns):
    pivot = pd.pivot_table(sales, values="revenue", index="region", columns="category", aggfunc="sum", fill_value=0)
    fig4, ax4 = plt.subplots(figsize=(6, 4))
    sns.heatmap(pivot, annot=True, fmt=".0f", cmap="rocket_r", ax=ax4)
    ax4.set_title("Revenue Heatmap: Region x Category")
    fig4
    return ax4, fig4, pivot


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Deliverable
        Combine the four figures into a single dashboard image using
        `plt.subplots(2, 2, figsize=(12, 8))` and save with `fig.savefig("sales_dashboard.png")`.

        ## Stretch Goal
        Add a week-over-week revenue % change column and highlight the best/worst week.
        """
    )
    return


if __name__ == "__main__":
    app.run()
