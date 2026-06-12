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
        # Lab 1: Customer Data Analysis

        **Goal:** Use Pandas to clean, segment, and analyze a customer dataset, producing
        a summary report a marketing manager could act on.

        **Dataset:** `resources/datasets/customers.csv`

        ## Tasks
        1. Load and inspect the data (shape, dtypes, missing values).
        2. Clean: handle missing values, ensure correct dtypes.
        3. Segment customers by `spend_tier` (Low/Medium/High) and `plan`.
        4. Compute: active customer rate, average spend per city, top 10 customers by spend.
        5. Summarize findings in markdown at the end.
        """
    )
    return


@app.cell
def __(pd):
    df = pd.read_csv("../../resources/datasets/customers.csv")
    print(df.shape)
    print(df.dtypes)
    print(df.isna().sum())
    return (df,)


@app.cell
def __(df):
    # Step 2: Clean (this dataset has no nulls by construction, but defensively handle them)
    df_clean = df.dropna(subset=["customer_id", "monthly_spend"]).copy()
    df_clean["signup_date"] = df_clean["signup_date"].astype("datetime64[ns]")
    df_clean.head()
    return (df_clean,)


@app.cell
def __(df_clean):
    # Step 3: Segmentation
    def spend_tier(spend):
        if spend > 200:
            return "High"
        elif spend > 50:
            return "Medium"
        return "Low"

    df_clean["spend_tier"] = df_clean["monthly_spend"].apply(spend_tier)
    segment_summary = df_clean.groupby(["plan", "spend_tier"]).size().unstack(fill_value=0)
    segment_summary
    return segment_summary, spend_tier


@app.cell
def __(df_clean):
    # Step 4: Key metrics
    active_rate = df_clean["is_active"].mean()
    avg_spend_by_city = df_clean.groupby("city")["monthly_spend"].mean().round(2).sort_values(ascending=False)
    top10 = df_clean.nlargest(10, "monthly_spend")[["customer_id", "name", "city", "plan", "monthly_spend"]]

    print(f"Active rate: {active_rate:.1%}")
    print("\nAvg spend by city:\n", avg_spend_by_city)
    print("\nTop 10 customers:\n", top10)
    return active_rate, avg_spend_by_city, top10


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Findings Summary (fill in based on output above)

        - X% of customers are active.
        - The highest-spending city is ___, suggesting ___.
        - The "High" spend tier is concentrated in the ___ plan, indicating an upsell
          opportunity for ___ plan users.

        ## Deliverable
        Export `segment_summary` and `avg_spend_by_city` to CSV for the marketing team:
        ```python
        segment_summary.to_csv("segment_summary.csv")
        avg_spend_by_city.to_csv("avg_spend_by_city.csv")
        ```
        """
    )
    return


if __name__ == "__main__":
    app.run()
