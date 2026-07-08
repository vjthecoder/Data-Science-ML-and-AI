import marimo

__generated_with = "0.9.0"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    import numpy as np
    import pandas as pd
    from sklearn.compose import ColumnTransformer
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import (
        GridSearchCV,
        RandomizedSearchCV,
        StratifiedKFold,
        cross_val_score,
        train_test_split,
    )
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import OneHotEncoder, StandardScaler
    return (
        ColumnTransformer,
        GridSearchCV,
        OneHotEncoder,
        Pipeline,
        RandomForestClassifier,
        RandomizedSearchCV,
        StandardScaler,
        StratifiedKFold,
        cross_val_score,
        mo,
        np,
        pd,
        train_test_split,
    )


@app.cell
def __(mo):
    mo.md(
        r"""
        # 07. Cross-Validation & Hyperparameter Tuning

        ## Theory

        **Level 1 (10-year-old):** Instead of testing your spelling on just ONE list of words,
        you test yourself on 5 different lists and average your scores — that gives a fairer
        idea of how good you really are.

        **Level 2 (College Student):** K-Fold cross-validation splits the training data into
        `k` folds; the model is trained on `k-1` folds and validated on the remaining fold,
        repeated `k` times. This gives a more robust performance estimate than a single
        train/test split. `StratifiedKFold` preserves class proportions in each fold —
        important for imbalanced classification. Hyperparameter tuning (`GridSearchCV`,
        `RandomizedSearchCV`) searches over hyperparameter combinations, evaluating each via
        cross-validation.

        **Level 3 (Industry Professional):** Cross-validation reduces variance in performance
        estimates but increases compute cost (`k`x training). For large datasets/expensive
        models, use `RandomizedSearchCV` or Bayesian optimization (Optuna) instead of
        exhaustive grid search. ALWAYS keep a final held-out test set untouched by CV/tuning
        for the true final evaluation.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Visual Explanation

        ```
        5-Fold Cross-Validation:
        Fold 1: [TEST][train][train][train][train]  -> score_1
        Fold 2: [train][TEST][train][train][train]  -> score_2
        Fold 3: [train][train][TEST][train][train]  -> score_3
        Fold 4: [train][train][train][TEST][train]  -> score_4
        Fold 5: [train][train][train][train][TEST]  -> score_5

        Final CV score = mean(score_1..score_5), report std too
        ```

        ```
        Data split:
        [-------- Train (for CV + tuning) --------][---- Test (final, untouched) ----]
        ```
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
    StratifiedKFold,
    cross_val_score,
    pd,
    train_test_split,
):
    df = pd.read_csv("../../resources/datasets/churn.csv")
    X = df.drop(columns=["customer_id", "churned"])
    y = df["churned"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    preprocess = ColumnTransformer([
        ("num", StandardScaler(), ["tenure_months", "monthly_charges", "support_tickets"]),
        ("cat", OneHotEncoder(handle_unknown="ignore"), ["contract_type", "plan"]),
    ])
    pipe = Pipeline([("preprocess", preprocess), ("model", RandomForestClassifier(random_state=42))])

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    scores = cross_val_score(pipe, X_train, y_train, cv=cv, scoring="f1")
    print("F1 per fold:", scores.round(3))
    print(f"Mean F1: {scores.mean():.3f} +/- {scores.std():.3f}")
    return X, X_test, X_train, cv, df, pipe, preprocess, scores, y, y_test, y_train


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Real-World Example: GridSearchCV for Random Forest
        """
    )
    return


@app.cell
def __(GridSearchCV, X_train, cv, pipe, y_train):
    param_grid = {
        "model__n_estimators": [50, 100, 200],
        "model__max_depth": [3, 5, None],
        "model__min_samples_split": [2, 5],
    }

    grid = GridSearchCV(pipe, param_grid, cv=cv, scoring="f1", n_jobs=-1)
    grid.fit(X_train, y_train)

    print("Best params:", grid.best_params_)
    print("Best CV F1:", round(grid.best_score_, 3))
    return grid, param_grid


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Final Evaluation on Held-Out Test Set
        """
    )
    return


@app.cell
def __(X_test, grid, y_test):
    from sklearn.metrics import classification_report, f1_score

    best_model = grid.best_estimator_
    test_preds = best_model.predict(X_test)
    print("Test F1:", round(f1_score(y_test, test_preds), 3))
    print(classification_report(y_test, test_preds))
    return best_model, classification_report, f1_score, test_preds


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Coding Exercise

        1. Use `RandomizedSearchCV` instead of `GridSearchCV` with the same `param_grid`
           (add `n_iter=6`) and compare the best score and runtime.
        2. Try `scoring="roc_auc"` instead of `"f1"` — does the best hyperparameter
           combination change?
        3. Explain in 2-3 sentences why the test set should NEVER be used during
           `GridSearchCV.fit()`.
        """
    )
    return


@app.cell
def __(RandomizedSearchCV, X_train, cv, param_grid, pipe, y_train):
    random_search = RandomizedSearchCV(pipe, param_grid, n_iter=6, cv=cv, scoring="f1", random_state=42, n_jobs=-1)
    random_search.fit(X_train, y_train)
    print("Best params (random search):", random_search.best_params_)
    print("Best CV F1:", round(random_search.best_score_, 3))
    return (random_search,)


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Assignment
        See `../assignments/week02_assignments.md` — Assignment 7.

        ## Interview Questions
        See `../../interview-prep/week02_ml_questions.md` — Section: Cross-Validation & Tuning.

        ## Industry Use Cases
        - Model selection before production deployment
        - Hyperparameter sweeps run as part of automated ML pipelines (CI for ML)

        ## Common Mistakes
        - Tuning on the test set (data leakage -> overly optimistic results)
        - Using `KFold` instead of `StratifiedKFold` for imbalanced classification
        - Exhaustive grid search on large hyperparameter spaces (too slow)

        ## Best Practices
        - Keep a final untouched test set
        - Use `StratifiedKFold` for classification
        - Start with `RandomizedSearchCV` for large search spaces, narrow down, then grid search
        """
    )
    return


if __name__ == "__main__":
    app.run()
