import marimo

__generated_with = "0.9.0"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    import pandas as pd
    return mo, pd


@app.cell
def __(mo):
    mo.md(
        r"""
        # 05. Pandas — DataFrames, Cleaning & Aggregation

        ## Theory

        **Level 1 (10-year-old):** A DataFrame is like a spreadsheet inside Python — rows and
        columns of data you can sort, filter, and add up.

        **Level 2 (College Student):** A `DataFrame` is a 2D labeled data structure built on
        NumPy arrays, with columns of potentially different types. Core operations: selection
        (`loc`/`iloc`), filtering (boolean masks), grouping (`groupby`), merging (`merge`/`join`),
        and handling missing data (`isna`, `fillna`, `dropna`).

        **Level 3 (Industry Professional):** Pandas is the workhorse of data wrangling in
        industry — ETL scripts, feature engineering, and reporting pipelines all rely on it.
        Performance matters: avoid `apply()` with Python functions on large data when a
        vectorized alternative exists; use `groupby().agg()` for multi-metric aggregations;
        be mindful of memory (`dtype` downcasting, categorical types for low-cardinality columns).
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Visual Explanation

        ```
        DataFrame:
        ┌────┬─────────┬────────┬──────────┐
        │ id │  city   │  plan  │  spend   │
        ├────┼─────────┼────────┼──────────┤
        │ 1  │ Mumbai  │  Pro   │  250.0   │
        │ 2  │ Pune    │  Free  │    0.0   │
        │ 3  │ Mumbai  │ Basic  │   49.0   │
        └────┴─────────┴────────┴──────────┘

        df.groupby("city")["spend"].mean()
        ->  Mumbai: 125.0
            Pune:     0.0
        ```
        """
    )
    return


@app.cell
def __(pd):
    df = pd.read_csv("../../resources/datasets/customers.csv")
    print(df.shape)
    df.head()
    return (df,)


@app.cell
def __(df):
    # Inspect & clean
    print(df.info())
    print("\nMissing values:\n", df.isna().sum())
    print("\nActive customers:", df["is_active"].sum())
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Real-World Example

        A growth team wants average monthly spend by city and plan, for ACTIVE customers only,
        sorted by spend descending — a classic "groupby + filter + sort" report.
        """
    )
    return


@app.cell
def __(df):
    active = df[df["is_active"] == 1]

    report = (
        active.groupby(["city", "plan"])["monthly_spend"]
        .mean()
        .round(2)
        .reset_index()
        .sort_values("monthly_spend", ascending=False)
    )
    report.head(10)
    return active, report


@app.cell
def __(df):
    # Filtering, selection, new columns
    high_value = df.loc[df["monthly_spend"] > 200, ["customer_id", "name", "city", "monthly_spend"]]
    print("High value customers:", len(high_value))

    df_copy = df.copy()
    df_copy["annual_spend"] = df_copy["monthly_spend"] * 12
    df_copy[["name", "monthly_spend", "annual_spend"]].head()
    return df_copy, high_value


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Coding Exercise

        Using `customers.csv`:
        1. Find the number of customers per `plan`.
        2. Find the average `age` of customers per `gender`.
        3. Create a new column `spend_tier`: "High" if `monthly_spend` > 200, "Medium" if > 50,
           else "Low". Then count customers per tier.
        """
    )
    return


@app.cell
def __(df, pd):
    plan_counts = df["plan"].value_counts()
    avg_age_by_gender = df.groupby("gender")["age"].mean().round(1)

    def spend_tier(spend):
        if spend > 200:
            return "High"
        elif spend > 50:
            return "Medium"
        return "Low"

    df["spend_tier"] = df["monthly_spend"].apply(spend_tier)
    tier_counts = df["spend_tier"].value_counts()

    print(plan_counts)
    print("\n", avg_age_by_gender)
    print("\n", tier_counts)
    return avg_age_by_gender, plan_counts, spend_tier, tier_counts


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Assignment
        See `../assignments/week01_assignments.md` — Assignment 5.

        ## Interview Questions
        See `../../interview-prep/week01_python_questions.md` — Section: Pandas.

        ## Industry Use Cases
        - Daily ETL reports (revenue by region, churn by segment)
        - Feature engineering for ML pipelines
        - Data quality checks before loading into a warehouse

        ## Common Mistakes
        - `SettingWithCopyWarning` from chained indexing (`df[df.x>1]['y'] = ...`)
        - Using `apply()` with Python functions when a vectorized op exists
        - Forgetting `.reset_index()` after `groupby`

        ## Best Practices
        - Use `.loc`/`.iloc` explicitly instead of chained indexing
        - Use `df.copy()` before mutating a filtered DataFrame
        - Use `groupby().agg({...})` for multiple aggregations at once
        """
    )
    return


if __name__ == "__main__":
    app.run()
