import marimo

__generated_with = "0.9.0"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    import matplotlib.pyplot as plt
    import pandas as pd
    from sklearn.compose import ColumnTransformer
    from sklearn.metrics import (
        ConfusionMatrixDisplay,
        classification_report,
        confusion_matrix,
        roc_auc_score,
        roc_curve,
    )
    from sklearn.model_selection import GridSearchCV, StratifiedKFold, train_test_split
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import OneHotEncoder, StandardScaler
    from xgboost import XGBClassifier
    return (
        ColumnTransformer,
        ConfusionMatrixDisplay,
        GridSearchCV,
        OneHotEncoder,
        Pipeline,
        StandardScaler,
        StratifiedKFold,
        XGBClassifier,
        classification_report,
        confusion_matrix,
        mo,
        pd,
        plt,
        roc_auc_score,
        roc_curve,
        train_test_split,
    )


@app.cell
def __(mo):
    mo.md(
        r"""
        # Lab 2: Customer Churn Prediction

        **Goal:** Build a tuned XGBoost model to predict customer churn, evaluate it
        thoroughly, and identify the key drivers of churn for the retention team.

        **Dataset:** `resources/datasets/churn.csv`

        ## Tasks
        1. EDA: churn rate overall and by `contract_type`.
        2. Build a preprocessing + XGBoost pipeline.
        3. Tune with `GridSearchCV` (5-fold stratified CV, scoring=`roc_auc`).
        4. Evaluate: classification report, ROC curve, confusion matrix.
        5. Report feature importances and translate them into retention recommendations.
        """
    )
    return


@app.cell
def __(pd):
    df = pd.read_csv("../../resources/datasets/churn.csv")
    print("Churn rate:", df["churned"].mean().round(3))
    print(df.groupby("contract_type")["churned"].mean().round(3))
    return (df,)


@app.cell
def __(ColumnTransformer, OneHotEncoder, StandardScaler, df, train_test_split):
    X = df.drop(columns=["customer_id", "churned"])
    y = df["churned"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    preprocess = ColumnTransformer([
        ("num", StandardScaler(), ["tenure_months", "monthly_charges", "support_tickets"]),
        ("cat", OneHotEncoder(handle_unknown="ignore"), ["contract_type", "plan"]),
    ])
    return X, X_test, X_train, preprocess, y, y_test, y_train


@app.cell
def __(GridSearchCV, Pipeline, StratifiedKFold, X_train, XGBClassifier, preprocess, y_train):
    pipe = Pipeline([("preprocess", preprocess), ("model", XGBClassifier(eval_metric="logloss", random_state=42))])
    param_grid = {
        "model__n_estimators": [100, 200],
        "model__max_depth": [3, 4, 5],
        "model__learning_rate": [0.05, 0.1],
    }
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    grid = GridSearchCV(pipe, param_grid, cv=cv, scoring="roc_auc", n_jobs=-1)
    grid.fit(X_train, y_train)
    print("Best params:", grid.best_params_)
    print("Best CV ROC-AUC:", round(grid.best_score_, 3))
    return cv, grid, param_grid, pipe


@app.cell
def __(ConfusionMatrixDisplay, X_test, classification_report, confusion_matrix, grid, plt, roc_auc_score, y_test):
    best = grid.best_estimator_
    preds = best.predict(X_test)
    proba = best.predict_proba(X_test)[:, 1]

    print(classification_report(y_test, preds))
    print("Test ROC-AUC:", round(roc_auc_score(y_test, proba), 3))

    cm = confusion_matrix(y_test, preds)
    fig, ax = plt.subplots(figsize=(4, 4))
    ConfusionMatrixDisplay(cm, display_labels=["No Churn", "Churn"]).plot(ax=ax)
    fig
    return ax, best, cm, fig, preds, proba


@app.cell
def __(X_test, plt, proba, roc_auc_score, roc_curve, y_test):
    fpr, tpr, _ = roc_curve(y_test, proba)
    fig2, ax2 = plt.subplots(figsize=(5, 5))
    ax2.plot(fpr, tpr, label=f"AUC={roc_auc_score(y_test, proba):.3f}")
    ax2.plot([0, 1], [0, 1], "k--")
    ax2.set_xlabel("False Positive Rate")
    ax2.set_ylabel("True Positive Rate")
    ax2.set_title("Churn Model ROC Curve")
    ax2.legend()
    fig2
    return ax2, fig2, fpr, tpr


@app.cell
def __(best):
    feature_names = best.named_steps["preprocess"].get_feature_names_out()
    importances = best.named_steps["model"].feature_importances_
    ranked = sorted(zip(feature_names, importances), key=lambda t: t[1], reverse=True)
    for fname, imp in ranked[:8]:
        print(f"{fname}: {imp:.3f}")
    return fname, feature_names, imp, importances, ranked


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Retention Recommendations (fill in based on feature importances)

        - Top driver of churn: **___** -> recommend ___
        - Customers on **month-to-month** contracts churn at ___% vs **two-year** at ___% ->
          recommend incentivizing longer contracts via ___
        - High `support_tickets` correlates with churn -> recommend proactive outreach after
          ___ tickets

        ## Stretch Goal
        Use the tuned model's `predict_proba` to flag the top 10% highest-risk currently-active
        customers (simulate by scoring the full dataset) for a retention campaign.
        """
    )
    return


if __name__ == "__main__":
    app.run()
