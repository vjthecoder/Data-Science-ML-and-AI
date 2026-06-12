import marimo

__generated_with = "0.9.0"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    import pandas as pd
    from sklearn.preprocessing import StandardScaler, OneHotEncoder
    from sklearn.model_selection import train_test_split
    return OneHotEncoder, StandardScaler, mo, pd, train_test_split


@app.cell
def __(mo):
    mo.md(
        r"""
        # 02. Feature Engineering

        ## Theory

        **Level 1 (10-year-old):** Sometimes raw information needs a little makeover before a
        computer can understand it — like turning "red", "blue", "green" into numbers, or
        making sure "height in cm" and "weight in kg" are on a similar scale.

        **Level 2 (College Student):** Feature engineering transforms raw data into model-ready
        inputs: encoding categorical variables (one-hot, ordinal), scaling numeric features
        (standardization, min-max), handling missing values (imputation), and creating new
        features from existing ones (e.g., `tenure_months / 12 = tenure_years`).

        **Level 3 (Industry Professional):** Feature engineering is often THE highest-leverage
        activity in a tabular ML project — more impactful than model choice. Critical rule:
        **fit transformers (scalers, encoders, imputers) on the training set ONLY**, then apply
        to validation/test sets, to avoid data leakage. Use `sklearn.pipeline.Pipeline` to
        enforce this automatically.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Visual Explanation

        ```
        WRONG (leakage):                    CORRECT:
        scaler.fit(all_data)                X_train, X_test = split(X)
        X_train, X_test = split(scaled)     scaler.fit(X_train)
                                             X_train_scaled = scaler.transform(X_train)
                                             X_test_scaled  = scaler.transform(X_test)
        ```

        ```
        Categorical "plan": ["Basic","Premium","Standard"]
        One-Hot Encoding ->  plan_Basic | plan_Premium | plan_Standard
                                  1            0              0
                                  0            1              0
                                  0            0              1
        ```
        """
    )
    return


@app.cell
def __(pd):
    df = pd.read_csv("../../resources/datasets/churn.csv")
    df.head()
    return (df,)


@app.cell
def __(df, train_test_split):
    # Step 1: split FIRST
    X = df.drop(columns=["customer_id", "churned"])
    y = df["churned"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    print(X_train.shape, X_test.shape)
    return X, X_test, X_train, y, y_test, y_train


@app.cell
def __(mo):
    mo.md("## Real-World Example: Encode & Scale (fit on train only)")
    return


@app.cell
def __(OneHotEncoder, StandardScaler, X_test, X_train):
    numeric_cols = ["tenure_months", "monthly_charges", "support_tickets"]
    categorical_cols = ["contract_type", "plan"]

    scaler = StandardScaler()
    X_train_num = scaler.fit_transform(X_train[numeric_cols])
    X_test_num = scaler.transform(X_test[numeric_cols])  # transform only, no fit!

    encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    X_train_cat = encoder.fit_transform(X_train[categorical_cols])
    X_test_cat = encoder.transform(X_test[categorical_cols])

    print("Numeric train shape:", X_train_num.shape)
    print("Categorical train shape:", X_train_cat.shape, "categories:", encoder.categories_)
    return (
        X_test_cat,
        X_test_num,
        X_train_cat,
        X_train_num,
        categorical_cols,
        encoder,
        numeric_cols,
        scaler,
    )


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Coding Exercise

        Using `leads.csv`:
        1. Create a new feature `engagement_score = website_visits + emails_opened * 2`.
        2. One-hot encode `source` and `industry` (fit on a train split only).
        3. Standardize `website_visits`, `emails_opened`, and `engagement_score`.
        4. Use `sklearn.pipeline.Pipeline` + `ColumnTransformer` to do steps 2-3 in one object.
        """
    )
    return


@app.cell
def __(pd, train_test_split):
    from sklearn.compose import ColumnTransformer
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import OneHotEncoder as OHE, StandardScaler as SS

    leads = pd.read_csv("../../resources/datasets/leads.csv")
    leads["engagement_score"] = leads["website_visits"] + leads["emails_opened"] * 2

    X_l = leads.drop(columns=["lead_id", "converted"])
    y_l = leads["converted"]
    X_l_train, X_l_test, y_l_train, y_l_test = train_test_split(X_l, y_l, test_size=0.2, random_state=42, stratify=y_l)

    numeric = ["website_visits", "emails_opened", "engagement_score"]
    categorical = ["source", "industry", "company_size", "budget_range"]

    preprocess = ColumnTransformer([
        ("num", SS(), numeric),
        ("cat", OHE(handle_unknown="ignore"), categorical),
    ])

    pipeline = Pipeline([("preprocess", preprocess)])
    X_l_train_transformed = pipeline.fit_transform(X_l_train)
    X_l_test_transformed = pipeline.transform(X_l_test)
    print("Transformed shapes:", X_l_train_transformed.shape, X_l_test_transformed.shape)
    return (
        ColumnTransformer,
        OHE,
        Pipeline,
        SS,
        X_l,
        X_l_test,
        X_l_test_transformed,
        X_l_train,
        X_l_train_transformed,
        categorical,
        leads,
        numeric,
        pipeline,
        preprocess,
        y_l,
        y_l_test,
        y_l_train,
    )


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Assignment
        See `../assignments/week02_assignments.md` — Assignment 2.

        ## Interview Questions
        See `../../interview-prep/week02_ml_questions.md` — Section: Feature Engineering.

        ## Industry Use Cases
        - Standardized preprocessing pipelines deployed alongside models (consistency at inference)
        - Feature stores that compute and serve engineered features consistently

        ## Common Mistakes
        - Fitting scalers/encoders on the full dataset before splitting
        - One-hot encoding high-cardinality columns (e.g., zip codes) without grouping
        - Forgetting `handle_unknown="ignore"` for categories unseen at training time

        ## Best Practices
        - Always wrap preprocessing in `Pipeline`/`ColumnTransformer`
        - Save fitted transformers alongside the model (e.g., via `joblib`)
        - Engineer features based on domain knowledge, not just automated combinations
        """
    )
    return


if __name__ == "__main__":
    app.run()
