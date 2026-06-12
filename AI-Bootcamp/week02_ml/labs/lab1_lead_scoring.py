import marimo

__generated_with = "0.9.0"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    import pandas as pd
    from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
    from sklearn.compose import ColumnTransformer
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import StandardScaler, OneHotEncoder
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import classification_report, roc_auc_score
    return (
        ColumnTransformer,
        GridSearchCV,
        LogisticRegression,
        OneHotEncoder,
        Pipeline,
        RandomForestClassifier,
        StandardScaler,
        StratifiedKFold,
        classification_report,
        mo,
        pd,
        roc_auc_score,
        train_test_split,
    )


@app.cell
def __(mo):
    mo.md(
        r"""
        # Lab 1: Lead Scoring Model

        **Goal:** Build an end-to-end pipeline that scores incoming sales leads by their
        probability of converting, so the sales team can prioritize outreach.

        **Dataset:** `resources/datasets/leads.csv`

        ## Tasks
        1. EDA: conversion rate overall and by `source`/`demo_requested`.
        2. Build a preprocessing + model pipeline (Logistic Regression baseline + Random Forest).
        3. Tune the Random Forest with `GridSearchCV`.
        4. Evaluate on a held-out test set (precision, recall, F1, ROC-AUC).
        5. Output a "lead score" (probability) for each test lead, sorted descending —
           this is what the sales team would receive.
        """
    )
    return


@app.cell
def __(pd):
    leads = pd.read_csv("../../resources/datasets/leads.csv")
    print("Overall conversion rate:", leads["converted"].mean().round(3))
    print(leads.groupby("source")["converted"].mean().round(3))
    return (leads,)


@app.cell
def __(ColumnTransformer, OneHotEncoder, StandardScaler, leads, train_test_split):
    X = leads.drop(columns=["lead_id", "converted"])
    y = leads["converted"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    numeric = ["website_visits", "emails_opened", "demo_requested"]
    categorical = ["source", "company_size", "industry", "budget_range"]
    preprocess = ColumnTransformer([
        ("num", StandardScaler(), numeric),
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical),
    ])
    return X, X_test, X_train, categorical, numeric, preprocess, y, y_test, y_train


@app.cell
def __(LogisticRegression, Pipeline, X_test, X_train, classification_report, preprocess, roc_auc_score, y_test, y_train):
    baseline = Pipeline([("preprocess", preprocess), ("model", LogisticRegression(max_iter=1000))])
    baseline.fit(X_train, y_train)
    base_preds = baseline.predict(X_test)
    base_proba = baseline.predict_proba(X_test)[:, 1]
    print("--- Logistic Regression Baseline ---")
    print(classification_report(y_test, base_preds))
    print("ROC-AUC:", round(roc_auc_score(y_test, base_proba), 3))
    return base_preds, base_proba, baseline


@app.cell
def __(GridSearchCV, Pipeline, RandomForestClassifier, StratifiedKFold, X_train, preprocess, y_train):
    rf_pipe = Pipeline([("preprocess", preprocess), ("model", RandomForestClassifier(random_state=42))])
    param_grid = {
        "model__n_estimators": [100, 200],
        "model__max_depth": [4, 6, None],
    }
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    grid = GridSearchCV(rf_pipe, param_grid, cv=cv, scoring="roc_auc", n_jobs=-1)
    grid.fit(X_train, y_train)
    print("Best params:", grid.best_params_, "Best CV ROC-AUC:", round(grid.best_score_, 3))
    return cv, grid, param_grid, rf_pipe


@app.cell
def __(X_test, classification_report, grid, roc_auc_score, y_test):
    best_model = grid.best_estimator_
    rf_preds = best_model.predict(X_test)
    rf_proba = best_model.predict_proba(X_test)[:, 1]
    print("--- Tuned Random Forest ---")
    print(classification_report(y_test, rf_preds))
    print("ROC-AUC:", round(roc_auc_score(y_test, rf_proba), 3))
    return best_model, rf_preds, rf_proba


@app.cell
def __(X_test, best_model, pd, rf_proba):
    lead_scores = X_test.copy()
    lead_scores["conversion_probability"] = rf_proba
    lead_scores = lead_scores.sort_values("conversion_probability", ascending=False)
    lead_scores.head(10)
    return (lead_scores,)


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Deliverable
        Export `lead_scores` to `lead_scores.csv` for the sales team:
        ```python
        lead_scores.to_csv("lead_scores.csv", index=False)
        ```

        ## Stretch Goal
        Compare the tuned Random Forest against an XGBoost model with the same
        `ColumnTransformer`. Which performs better on ROC-AUC, and is the difference
        meaningful given the dataset size?
        """
    )
    return


if __name__ == "__main__":
    app.run()
