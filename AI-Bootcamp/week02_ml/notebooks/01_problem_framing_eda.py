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
        # 01. Problem Framing & EDA

        ## Theory

        **Level 1 (10-year-old):** Before you build a robot to sort your toys, you first look
        at ALL your toys and figure out what kinds you have — that's exploring the data before
        building anything.

        **Level 2 (College Student):** ML problem framing means translating a business question
        ("which customers will cancel?") into a supervised learning task (binary classification
        with `churned` as the target). EDA (Exploratory Data Analysis) means examining
        distributions, missing values, correlations, and class balance BEFORE modeling.

        **Level 3 (Industry Professional):** Most ML project failures stem from poor problem
        framing — wrong target variable, label leakage, or a target that doesn't map to a
        decision someone will actually act on. EDA should answer: What's the target? Is it
        balanced? What features are available AT PREDICTION TIME (not after the fact — avoid
        leakage)? Are there data quality issues?
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Visual Explanation

        ```
        Business Question          ML Framing
        ---------------------------------------------------------
        "Which leads will buy?"  -> Binary classification
                                     target = converted (0/1)

        "How much will a customer
         spend next month?"      -> Regression
                                     target = next_month_spend

        "Group similar customers" -> Clustering (unsupervised)
                                      no target variable
        ```
        """
    )
    return


@app.cell
def __(pd):
    df = pd.read_csv("../../resources/datasets/churn.csv")
    print(df.shape)
    df.head()
    return (df,)


@app.cell
def __(df):
    # EDA: target balance, missing values, summary stats
    print("Churn rate:", df["churned"].mean().round(3))
    print("\nMissing values:\n", df.isna().sum())
    print("\nNumeric summary:\n", df.describe())
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Real-World Example

        A telecom company frames "reduce churn" as: *predict, for each active customer this
        month, the probability they cancel next month, using only data available as of today*
        (tenure, contract type, support tickets, monthly charges — NOT future billing data,
        which would be leakage).
        """
    )
    return


@app.cell
def __(df, pd):
    # Check feature-target relationships
    churn_by_contract = df.groupby("contract_type")["churned"].mean().round(3)
    churn_by_tickets = df.groupby(pd.cut(df["support_tickets"], bins=[-1,0,2,4,8]))["churned"].mean().round(3)
    print(churn_by_contract)
    print("\n", churn_by_tickets)
    return churn_by_contract, churn_by_tickets


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Coding Exercise

        Using `leads.csv`:
        1. Compute the overall conversion rate.
        2. Check conversion rate by `source` and by `demo_requested`.
        3. Identify any columns with missing values.
        4. State in 1-2 sentences: is this dataset balanced? What's the strongest-looking
           predictor based on this EDA?
        """
    )
    return


@app.cell
def __(pd):
    leads = pd.read_csv("../../resources/datasets/leads.csv")
    print("Conversion rate:", leads["converted"].mean().round(3))
    print(leads.groupby("source")["converted"].mean().round(3))
    print(leads.groupby("demo_requested")["converted"].mean().round(3))
    print(leads.isna().sum())
    return (leads,)


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Assignment
        See `../assignments/week02_assignments.md` — Assignment 1.

        ## Interview Questions
        See `../../interview-prep/week02_ml_questions.md` — Section: Problem Framing & EDA.

        ## Industry Use Cases
        - Defining the modeling target correctly (e.g., 30-day vs 90-day churn)
        - Spotting label leakage before it costs weeks of wasted effort
        - Communicating data quality issues to stakeholders early

        ## Common Mistakes
        - Using features that wouldn't be available at prediction time (leakage)
        - Ignoring class imbalance until evaluation time
        - Skipping EDA and jumping straight to modeling

        ## Best Practices
        - Always check target balance first
        - Visualize feature-target relationships before modeling
        - Document the prediction-time feature availability assumption
        """
    )
    return


if __name__ == "__main__":
    app.run()
