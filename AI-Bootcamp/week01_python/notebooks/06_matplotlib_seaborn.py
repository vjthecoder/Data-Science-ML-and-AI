import marimo

__generated_with = "0.9.0"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    import matplotlib.pyplot as plt
    import pandas as pd
    import seaborn as sns
    return mo, pd, plt, sns


@app.cell
def __(mo):
    mo.md(
        r"""
        # 06. Matplotlib & Seaborn — Visualization

        ## Theory

        **Level 1 (10-year-old):** Charts turn boring number tables into pictures, so you can SEE
        patterns — like which day had the most ice cream sales.

        **Level 2 (College Student):** Matplotlib is the low-level plotting library (figures,
        axes, full control). Seaborn is built on top of Matplotlib and provides high-level,
        statistically-aware plots (bar plots with confidence intervals, distributions, heatmaps)
        with better defaults.

        **Level 3 (Industry Professional):** Good visualizations are a communication tool for
        stakeholders — choose the right chart for the question (trend -> line, comparison -> bar,
        distribution -> histogram/box, relationship -> scatter, correlation -> heatmap). Always
        label axes, add titles, and avoid misleading scales.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Visual Explanation

        ```
        Question                  -> Chart type
        --------------------------------------
        Trend over time           -> Line chart
        Compare categories        -> Bar chart
        Distribution of a value   -> Histogram / KDE / Box plot
        Relationship between vars -> Scatter plot
        Correlation matrix        -> Heatmap
        ```
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
def __(mo):
    mo.md("## Simple Example: Bar chart of revenue by category")
    return


@app.cell
def __(plt, sales, sns):
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    cat_revenue = sales.groupby("category")["revenue"].sum().sort_values(ascending=False)
    sns.barplot(x=cat_revenue.index, y=cat_revenue.values, ax=ax1)
    ax1.set_title("Total Revenue by Category")
    ax1.set_xlabel("Category")
    ax1.set_ylabel("Revenue (₹)")
    fig1
    return ax1, cat_revenue, fig1


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Real-World Example: Monthly Revenue Trend (Sales Dashboard)

        Executives want a single chart showing whether revenue is trending up or down month
        over month — a line chart is the right tool.
        """
    )
    return


@app.cell
def __(plt, sales):
    monthly = sales.set_index("date").resample("M")["revenue"].sum()

    fig2, ax2 = plt.subplots(figsize=(7, 4))
    ax2.plot(monthly.index, monthly.values, marker="o")
    ax2.set_title("Monthly Revenue Trend")
    ax2.set_xlabel("Month")
    ax2.set_ylabel("Revenue (₹)")
    fig2.autofmt_xdate()
    fig2
    return ax2, fig2, monthly


@app.cell
def __(plt, sales, sns):
    fig3, axes = plt.subplots(1, 2, figsize=(10, 4))
    sns.histplot(sales["revenue"], bins=20, ax=axes[0])
    axes[0].set_title("Revenue Distribution")

    sns.boxplot(x="region", y="revenue", data=sales, ax=axes[1])
    axes[1].set_title("Revenue by Region")
    fig3.tight_layout()
    fig3
    return axes, fig3


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Coding Exercise

        Using `sales.csv`:
        1. Create a bar chart of total `units` sold per `region`.
        2. Create a heatmap of total revenue with `region` as rows and `category` as columns
           (hint: use `pd.pivot_table` then `sns.heatmap`).
        """
    )
    return


@app.cell
def __(pd, plt, sales, sns):
    fig4, ax4 = plt.subplots(figsize=(6, 4))
    units_by_region = sales.groupby("region")["units"].sum()
    sns.barplot(x=units_by_region.index, y=units_by_region.values, ax=ax4)
    ax4.set_title("Total Units Sold by Region")
    fig4

    pivot = pd.pivot_table(sales, values="revenue", index="region", columns="category", aggfunc="sum", fill_value=0)
    fig5, ax5 = plt.subplots(figsize=(6, 4))
    sns.heatmap(pivot, annot=True, fmt=".0f", cmap="YlGnBu", ax=ax5)
    ax5.set_title("Revenue Heatmap (Region x Category)")
    fig5
    return ax4, ax5, fig4, fig5, pivot, units_by_region


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Assignment
        See `../assignments/week01_assignments.md` — Assignment 6.

        ## Interview Questions
        See `../../interview-prep/week01_python_questions.md` — Section: Visualization.

        ## Industry Use Cases
        - Executive dashboards (revenue trends, KPI summaries)
        - EDA before model building (distributions, correlations)
        - Anomaly spotting (outliers in box plots)

        ## Common Mistakes
        - Truncated/misleading y-axes that exaggerate differences
        - Too many categories crammed into one pie chart
        - Missing titles/axis labels

        ## Best Practices
        - Always label axes and add a title
        - Use color purposefully (highlight, not decorate)
        - Choose chart type based on the question being answered
        """
    )
    return


if __name__ == "__main__":
    app.run()
