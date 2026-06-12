import marimo

__generated_with = "0.9.0"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    from sklearn.metrics import (
        confusion_matrix, ConfusionMatrixDisplay, classification_report,
        roc_curve, roc_auc_score, precision_recall_curve,
    )
    return (
        ConfusionMatrixDisplay,
        classification_report,
        confusion_matrix,
        mo,
        np,
        pd,
        plt,
        precision_recall_curve,
        roc_auc_score,
        roc_curve,
    )


@app.cell
def __(mo):
    mo.md(
        r"""
        # 06. Evaluation Metrics — Classification & Regression

        ## Theory

        **Level 1 (10-year-old):** If you guess "will it rain tomorrow?" every single day, how
        do you know if you're a good guesser? You count how often you were right, how often
        you said "yes" correctly, and how often you missed a rainy day.

        **Level 2 (College Student):**
        - **Regression:** RMSE (penalizes large errors more), MAE (average absolute error),
          R^2 (variance explained).
        - **Classification:** Accuracy (overall correct %), Precision (of predicted positives,
          how many are correct), Recall (of actual positives, how many were caught), F1
          (harmonic mean of precision/recall), ROC-AUC (ranking quality across thresholds).

        **Level 3 (Industry Professional):** Metric choice MUST reflect business cost.
        Fraud detection prioritizes recall (catch fraud, even with false positives). Spam
        filters prioritize precision (don't block legitimate email). On imbalanced data,
        accuracy is misleading — a model predicting "no churn" for everyone could be 95%
        "accurate" but useless. Always inspect the confusion matrix.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Visual Explanation

        ```
        Confusion Matrix:
                          Predicted: No    Predicted: Yes
        Actual: No        TN (correct)     FP (false alarm)
        Actual: Yes       FN (missed!)     TP (correct)

        Precision = TP / (TP + FP)   "Of what I flagged, how much was right?"
        Recall    = TP / (TP + FN)   "Of all actual positives, how many did I catch?"
        F1        = 2 * P * R / (P + R)
        ```
        """
    )
    return


@app.cell
def __(ConfusionMatrixDisplay, classification_report, confusion_matrix, plt):
    # Simple Example: toy predictions
    y_true = [0, 1, 1, 0, 1, 0, 1, 1, 0, 0]
    y_pred = [0, 1, 0, 0, 1, 1, 1, 1, 0, 0]

    cm = confusion_matrix(y_true, y_pred)
    print(cm)
    print(classification_report(y_true, y_pred, target_names=["No", "Yes"]))

    fig, ax = plt.subplots(figsize=(4, 4))
    ConfusionMatrixDisplay(cm, display_labels=["No", "Yes"]).plot(ax=ax)
    fig
    return ax, cm, fig, y_pred, y_true


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Real-World Example: ROC Curve for Churn Model
        """
    )
    return


@app.cell
def __(pd):
    from sklearn.model_selection import train_test_split
    from sklearn.compose import ColumnTransformer
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import StandardScaler, OneHotEncoder
    from sklearn.ensemble import RandomForestClassifier

    df = pd.read_csv("../../resources/datasets/churn.csv")
    X = df.drop(columns=["customer_id", "churned"])
    y = df["churned"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    preprocess = ColumnTransformer([
        ("num", StandardScaler(), ["tenure_months", "monthly_charges", "support_tickets"]),
        ("cat", OneHotEncoder(handle_unknown="ignore"), ["contract_type", "plan"]),
    ])
    pipe = Pipeline([("preprocess", preprocess), ("model", RandomForestClassifier(n_estimators=100, random_state=42))])
    pipe.fit(X_train, y_train)
    y_proba = pipe.predict_proba(X_test)[:, 1]
    return (
        ColumnTransformer,
        OneHotEncoder,
        Pipeline,
        RandomForestClassifier,
        StandardScaler,
        X,
        X_test,
        X_train,
        df,
        pipe,
        preprocess,
        train_test_split,
        y,
        y_proba,
        y_test,
        y_train,
    )


@app.cell
def __(plt, roc_auc_score, roc_curve, y_proba, y_test):
    fpr, tpr, thresholds = roc_curve(y_test, y_proba)
    auc = roc_auc_score(y_test, y_proba)

    fig2, ax2 = plt.subplots(figsize=(5, 5))
    ax2.plot(fpr, tpr, label=f"ROC (AUC={auc:.3f})")
    ax2.plot([0, 1], [0, 1], "k--", label="Random")
    ax2.set_xlabel("False Positive Rate")
    ax2.set_ylabel("True Positive Rate")
    ax2.set_title("ROC Curve — Churn Model")
    ax2.legend()
    fig2
    return ax2, auc, fig2, fpr, thresholds, tpr


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Coding Exercise

        1. Plot a precision-recall curve for the churn model (`precision_recall_curve`).
        2. Find the probability threshold that maximizes F1 score (try thresholds 0.1 to 0.9
           in steps of 0.05).
        3. Explain: if the business cost of missing a churner is much higher than the cost of
           a false alarm, should you raise or lower the classification threshold?
        """
    )
    return


@app.cell
def __(np, plt, precision_recall_curve, y_proba, y_test):
    from sklearn.metrics import f1_score

    precisions, recalls, pr_thresholds = precision_recall_curve(y_test, y_proba)

    fig3, ax3 = plt.subplots(figsize=(5, 5))
    ax3.plot(recalls, precisions)
    ax3.set_xlabel("Recall")
    ax3.set_ylabel("Precision")
    ax3.set_title("Precision-Recall Curve")
    fig3

    best_f1, best_t = 0, 0.5
    for t in np.arange(0.1, 0.95, 0.05):
        f1 = f1_score(y_test, (y_proba >= t).astype(int))
        if f1 > best_f1:
            best_f1, best_t = f1, t
    print(f"Best threshold: {best_t:.2f}, F1: {best_f1:.3f}")
    return ax3, best_f1, best_t, f1, f1_score, fig3, pr_thresholds, precisions, recalls, t


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Assignment
        See `../assignments/week02_assignments.md` — Assignment 6.

        ## Interview Questions
        See `../../interview-prep/week02_ml_questions.md` — Section: Evaluation Metrics.

        ## Industry Use Cases
        - Choosing thresholds for fraud/churn alerts based on cost-benefit analysis
        - Reporting model performance to non-technical stakeholders via confusion matrices

        ## Common Mistakes
        - Reporting only accuracy on imbalanced datasets
        - Using the default 0.5 threshold without considering business costs
        - Confusing precision and recall

        ## Best Practices
        - Always show the confusion matrix alongside summary metrics
        - Pick thresholds based on business cost trade-offs, not defaults
        - For regression, report RMSE AND MAE (different sensitivity to outliers)
        """
    )
    return


if __name__ == "__main__":
    app.run()
