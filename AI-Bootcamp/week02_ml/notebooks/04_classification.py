import marimo

__generated_with = "0.9.0"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    import pandas as pd
    from sklearn.compose import ColumnTransformer
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import (
        accuracy_score,
        f1_score,
        precision_score,
        recall_score,
        roc_auc_score,
    )
    from sklearn.model_selection import train_test_split
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import OneHotEncoder, StandardScaler
    from sklearn.tree import DecisionTreeClassifier
    from xgboost import XGBClassifier
    return (
        ColumnTransformer,
        DecisionTreeClassifier,
        LogisticRegression,
        OneHotEncoder,
        Pipeline,
        RandomForestClassifier,
        StandardScaler,
        XGBClassifier,
        accuracy_score,
        f1_score,
        mo,
        pd,
        precision_score,
        recall_score,
        roc_auc_score,
        train_test_split,
    )


@app.cell
def __(mo):
    mo.md(
        r"""
        # 04. Classification — Logistic Regression, Trees, Random Forest, XGBoost

        ## Theory

        **Level 1 (10-year-old):** Classification is sorting things into boxes — "will this
        customer leave or stay?" Logistic regression draws a curvy line to separate the boxes.
        A decision tree asks yes/no questions until it's confident which box something belongs
        in. A random forest asks LOTS of trees and takes a vote.

        **Level 2 (College Student):** Logistic regression models `P(y=1|x)` via the sigmoid
        function of a linear combination of features. Decision trees split on feature
        thresholds to maximize information gain (or Gini impurity reduction). Random Forest is
        an ensemble of decision trees trained on bootstrapped samples (bagging). XGBoost is a
        gradient-boosted ensemble — trees trained sequentially, each correcting the previous
        ones' errors.

        **Level 3 (Industry Professional):** Logistic regression remains a strong, fast,
        interpretable baseline — often a regulatory requirement in credit/insurance. Random
        Forest is robust and requires little tuning. XGBoost/LightGBM dominate tabular ML
        competitions and production systems due to high accuracy and built-in handling of
        missing values, but require careful tuning and are less interpretable (use SHAP for
        explainability).
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Visual Explanation

        ```
        Logistic Regression:           Decision Tree:
        sigmoid(w·x + b) -> P(y=1)            tenure < 12?
              1 |        ___                 /          \
                |      _/                  Yes           No
              0 |_____/                  churn=0.7    contract=2yr?
                +-------------- x                     /        \
                                                    Yes          No
                                                  churn=0.1   churn=0.5

        Random Forest = many trees, majority vote
        XGBoost = trees trained sequentially, each fixing prior errors
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
def __(ColumnTransformer, OneHotEncoder, StandardScaler, df, train_test_split):
    X = df.drop(columns=["customer_id", "churned"])
    y = df["churned"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    numeric = ["tenure_months", "monthly_charges", "support_tickets"]
    categorical = ["contract_type", "plan"]
    preprocess = ColumnTransformer([
        ("num", StandardScaler(), numeric),
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical),
    ])
    return X, X_test, X_train, categorical, numeric, preprocess, y, y_test, y_train


@app.cell
def __(mo):
    mo.md("## Real-World Example: Compare 4 Classifiers on Churn Prediction")
    return


@app.cell
def __(
    DecisionTreeClassifier,
    LogisticRegression,
    Pipeline,
    RandomForestClassifier,
    XGBClassifier,
    X_test,
    X_train,
    accuracy_score,
    f1_score,
    precision_score,
    preprocess,
    recall_score,
    roc_auc_score,
    y_test,
    y_train,
):
    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000),
        "Decision Tree": DecisionTreeClassifier(max_depth=5, random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
        "XGBoost": XGBClassifier(n_estimators=100, max_depth=4, eval_metric="logloss", random_state=42),
    }

    results = []
    for mname, clf in models.items():
        pipe = Pipeline([("preprocess", preprocess), ("model", clf)])
        pipe.fit(X_train, y_train)
        preds = pipe.predict(X_test)
        proba = pipe.predict_proba(X_test)[:, 1]
        results.append({
            "model": mname,
            "accuracy": round(accuracy_score(y_test, preds), 3),
            "precision": round(precision_score(y_test, preds), 3),
            "recall": round(recall_score(y_test, preds), 3),
            "f1": round(f1_score(y_test, preds), 3),
            "roc_auc": round(roc_auc_score(y_test, proba), 3),
        })

    import pandas as pd
    pd.DataFrame(results)
    return clf, mname, models, pd, pipe, preds, proba, results


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Coding Exercise

        Using `leads.csv`:
        1. Build a pipeline (preprocessing + `RandomForestClassifier`) to predict `converted`.
        2. Report accuracy, precision, recall, F1, and ROC-AUC on a held-out test set.
        3. Print the top 5 most important features (`model.feature_importances_` after fitting
           — note you'll need to get feature names from the `ColumnTransformer`).
        """
    )
    return


@app.cell
def __(
    ColumnTransformer,
    OneHotEncoder,
    Pipeline,
    RandomForestClassifier,
    StandardScaler,
    accuracy_score,
    f1_score,
    pd,
    precision_score,
    recall_score,
    roc_auc_score,
    train_test_split,
):
    leads = pd.read_csv("../../resources/datasets/leads.csv")
    X_l = leads.drop(columns=["lead_id", "converted"])
    y_l = leads["converted"]
    Xl_train, Xl_test, yl_train, yl_test = train_test_split(X_l, y_l, test_size=0.2, random_state=42, stratify=y_l)

    num_l = ["website_visits", "emails_opened", "demo_requested"]
    cat_l = ["source", "company_size", "industry", "budget_range"]
    prep_l = ColumnTransformer([("num", StandardScaler(), num_l), ("cat", OneHotEncoder(handle_unknown="ignore"), cat_l)])

    rf_pipe = Pipeline([("preprocess", prep_l), ("model", RandomForestClassifier(n_estimators=100, random_state=42))])
    rf_pipe.fit(Xl_train, yl_train)
    l_preds = rf_pipe.predict(Xl_test)
    l_proba = rf_pipe.predict_proba(Xl_test)[:, 1]

    print("Accuracy:", round(accuracy_score(yl_test, l_preds), 3))
    print("Precision:", round(precision_score(yl_test, l_preds), 3))
    print("Recall:", round(recall_score(yl_test, l_preds), 3))
    print("F1:", round(f1_score(yl_test, l_preds), 3))
    print("ROC-AUC:", round(roc_auc_score(yl_test, l_proba), 3))

    feature_names = rf_pipe.named_steps["preprocess"].get_feature_names_out()
    importances = rf_pipe.named_steps["model"].feature_importances_
    top5 = sorted(zip(feature_names, importances), key=lambda t: t[1], reverse=True)[:5]
    print("\nTop 5 features:", top5)
    return (
        Xl_test,
        Xl_train,
        cat_l,
        feature_names,
        importances,
        l_preds,
        l_proba,
        leads,
        num_l,
        prep_l,
        rf_pipe,
        top5,
        X_l,
        y_l,
        yl_test,
        yl_train,
    )


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Assignment
        See `../assignments/week02_assignments.md` — Assignment 4.

        ## Interview Questions
        See `../../interview-prep/week02_ml_questions.md` — Section: Classification.

        ## Industry Use Cases
        - Churn prediction, fraud detection, lead scoring, medical diagnosis support
        - Credit risk models (often require interpretable logistic regression)

        ## Common Mistakes
        - Using accuracy as the sole metric on imbalanced data
        - Not stratifying train/test splits for classification
        - Overfitting deep trees / too many XGBoost rounds without early stopping

        ## Best Practices
        - Choose metrics aligned with business cost (e.g., recall for fraud detection)
        - Use `class_weight="balanced"` or resampling for imbalanced data
        - Use early stopping + validation set for gradient boosting
        """
    )
    return


if __name__ == "__main__":
    app.run()
