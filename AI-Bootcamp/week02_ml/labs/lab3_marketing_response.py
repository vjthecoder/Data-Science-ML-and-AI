import marimo

__generated_with = "0.9.0"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    import pandas as pd
    import matplotlib.pyplot as plt
    from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
    from sklearn.compose import ColumnTransformer
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import StandardScaler, OneHotEncoder
    from sklearn.linear_model import LogisticRegression
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import classification_report, roc_auc_score
    return (
        ColumnTransformer,
        LogisticRegression,
        OneHotEncoder,
        Pipeline,
        RandomForestClassifier,
        StandardScaler,
        StratifiedKFold,
        classification_report,
        cross_val_score,
        mo,
        pd,
        plt,
        roc_auc_score,
        train_test_split,
    )


@app.cell
def __(mo):
    mo.md(
        r"""
        # Lab 3: Marketing Response Prediction

        **Goal:** Predict which customers will respond to a marketing campaign
        (`resources/datasets/marketing_response.csv`), using cross-validation to compare
        models before final evaluation.

        ## Tasks
        1. EDA: response rate overall and by `channel_preference`.
        2. Build pipelines for Logistic Regression and Random Forest.
        3. Compare both using 5-fold stratified cross-validation (ROC-AUC).
        4. Pick the better model, evaluate on the test set, and plot response rate by
           `channel_preference` to recommend targeting.
        """
    )
    return


@app.cell
def __(pd):
    mkt = pd.read_csv("../../resources/datasets/marketing_response.csv")
    print("Response rate:", mkt["responded"].mean().round(3))
    print(mkt.groupby("channel_preference")["responded"].mean().round(3))
    return (mkt,)


@app.cell
def __(ColumnTransformer, OneHotEncoder, StandardScaler, mkt, train_test_split):
    X = mkt.drop(columns=["customer_id", "responded"])
    y = mkt["responded"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    preprocess = ColumnTransformer([
        ("num", StandardScaler(), ["age", "income", "past_purchases", "email_engagement_score"]),
        ("cat", OneHotEncoder(handle_unknown="ignore"), ["channel_preference"]),
    ])
    return X, X_test, X_train, preprocess, y, y_test, y_train


@app.cell
def __(
    LogisticRegression,
    Pipeline,
    RandomForestClassifier,
    StratifiedKFold,
    X_train,
    cross_val_score,
    preprocess,
    y_train,
):
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    candidates = {
        "Logistic Regression": LogisticRegression(max_iter=1000),
        "Random Forest": RandomForestClassifier(n_estimators=150, max_depth=6, random_state=42),
    }

    for cname, clf in candidates.items():
        pipe = Pipeline([("preprocess", preprocess), ("model", clf)])
        scores = cross_val_score(pipe, X_train, y_train, cv=cv, scoring="roc_auc")
        print(f"{cname}: ROC-AUC = {scores.mean():.3f} +/- {scores.std():.3f}")
    return candidates, clf, cname, cv, pipe, scores


@app.cell
def __(Pipeline, RandomForestClassifier, X_test, X_train, classification_report, preprocess, roc_auc_score, y_test, y_train):
    final_model = Pipeline([
        ("preprocess", preprocess),
        ("model", RandomForestClassifier(n_estimators=150, max_depth=6, random_state=42)),
    ])
    final_model.fit(X_train, y_train)
    preds = final_model.predict(X_test)
    proba = final_model.predict_proba(X_test)[:, 1]
    print(classification_report(y_test, preds))
    print("Test ROC-AUC:", round(roc_auc_score(y_test, proba), 3))
    return final_model, preds, proba


@app.cell
def __(mkt, plt):
    fig, ax = plt.subplots(figsize=(6, 4))
    response_by_channel = mkt.groupby("channel_preference")["responded"].mean().sort_values(ascending=False)
    ax.bar(response_by_channel.index, response_by_channel.values, color="teal")
    ax.set_title("Response Rate by Channel Preference")
    ax.set_ylabel("Response Rate")
    fig
    return ax, fig, response_by_channel


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Targeting Recommendation

        - Highest-responding channel: **___** -> prioritize this channel for the next campaign.
        - The Random Forest model's ROC-AUC (___) is (better/worse) than Logistic Regression
          (___) by cross-validation — recommend using ___ for production scoring.

        ## Stretch Goal
        Add a feature `income_per_purchase = income / (past_purchases + 1)` and re-run
        cross-validation — does it improve ROC-AUC?
        """
    )
    return


if __name__ == "__main__":
    app.run()
