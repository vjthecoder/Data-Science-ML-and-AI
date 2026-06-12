import marimo

__generated_with = "0.9.0"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    import pandas as pd
    import numpy as np
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LinearRegression, Ridge, Lasso
    from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
    return (
        Lasso,
        LinearRegression,
        Ridge,
        mean_absolute_error,
        mean_squared_error,
        mo,
        np,
        pd,
        r2_score,
        train_test_split,
    )


@app.cell
def __(mo):
    mo.md(
        r"""
        # 03. Regression — Linear, Ridge, Lasso

        ## Theory

        **Level 1 (10-year-old):** Regression is drawing the "best fit" line through a bunch
        of dots, so you can guess where a new dot would land.

        **Level 2 (College Student):** Linear regression models `y = w·x + b`, minimizing sum
        of squared errors. Ridge adds an L2 penalty (`+ alpha * sum(w^2)`) to shrink
        coefficients and reduce overfitting. Lasso adds an L1 penalty (`+ alpha * sum(|w|)`),
        which can shrink some coefficients exactly to zero (feature selection).

        **Level 3 (Industry Professional):** Linear models remain widely used in production for
        their interpretability, speed, and stability — especially in regulated industries
        (finance, insurance) where model explainability is required. Ridge/Lasso (and
        ElasticNet) are essential when features are correlated (multicollinearity) or when
        you want automatic feature selection.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Visual Explanation

        ```
        y
        |        *
        |      *   *
        |    *   *      <- regression line: y = w*x + b
        |  *    *
        |________________ x

        Ridge: penalizes large w -> smoother, more robust line
        Lasso: can zero-out unimportant features entirely
        ```
        """
    )
    return


@app.cell
def __(np):
    # Simple Example: synthetic linear relationship
    rng = np.random.default_rng(0)
    x = rng.uniform(0, 10, 100)
    y = 3 * x + 5 + rng.normal(0, 2, 100)  # y = 3x + 5 + noise
    return rng, x, y


@app.cell
def __(LinearRegression, mean_squared_error, np, r2_score, x, y):
    X = x.reshape(-1, 1)
    model = LinearRegression()
    model.fit(X, y)
    preds = model.predict(X)

    print("Coefficient (slope):", model.coef_[0].round(3))
    print("Intercept:", model.intercept_.round(3))
    print("RMSE:", np.sqrt(mean_squared_error(y, preds)).round(3))
    print("R^2:", r2_score(y, preds).round(3))
    return X, model, preds


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Real-World Example: Predicting Monthly Charges from Tenure & Support Tickets

        A telecom analytics team wants to predict `monthly_charges` from `tenure_months` and
        `support_tickets` — useful for spotting customers whose charges deviate unusually from
        the model's expectation (potential billing errors).
        """
    )
    return


@app.cell
def __(Lasso, Ridge, LinearRegression, mean_absolute_error, pd, train_test_split):
    df = pd.read_csv("../../resources/datasets/churn.csv")
    X_r = df[["tenure_months", "support_tickets"]]
    y_r = df["monthly_charges"]

    X_train, X_test, y_train, y_test = train_test_split(X_r, y_r, test_size=0.2, random_state=42)

    for name, reg in [("Linear", LinearRegression()), ("Ridge", Ridge(alpha=1.0)), ("Lasso", Lasso(alpha=0.1))]:
        reg.fit(X_train, y_train)
        mae = mean_absolute_error(y_test, reg.predict(X_test))
        print(f"{name}: MAE={mae:.2f}, coefs={reg.coef_.round(3)}")
    return X_r, X_test, X_train, df, mae, name, reg, y_r, y_test, y_train


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Coding Exercise

        Using `sales.csv` (Week 1 dataset):
        1. Predict `revenue` from `units` and `unit_price` using `LinearRegression`.
        2. Report RMSE, MAE, and R^2 on a held-out test set.
        3. Compare against a Ridge model with `alpha=1.0` — does regularization help here?
           Why or why not (hint: think about how `revenue` relates to `units * unit_price`)?
        """
    )
    return


@app.cell
def __(LinearRegression, Ridge, mean_absolute_error, mean_squared_error, np, pd, r2_score, train_test_split):
    sales = pd.read_csv("../../resources/datasets/sales.csv")
    X_s = sales[["units", "unit_price"]]
    y_s = sales["revenue"]
    X_s_train, X_s_test, y_s_train, y_s_test = train_test_split(X_s, y_s, test_size=0.2, random_state=42)

    for sname, sreg in [("Linear", LinearRegression()), ("Ridge", Ridge(alpha=1.0))]:
        sreg.fit(X_s_train, y_s_train)
        spreds = sreg.predict(X_s_test)
        rmse = np.sqrt(mean_squared_error(y_s_test, spreds))
        mae_s = mean_absolute_error(y_s_test, spreds)
        r2 = r2_score(y_s_test, spreds)
        print(f"{sname}: RMSE={rmse:.2f}, MAE={mae_s:.2f}, R2={r2:.4f}")
    return X_s, X_s_test, X_s_train, mae_s, r2, rmse, sales, sname, spreds, sreg, y_s, y_s_test, y_s_train


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Assignment
        See `../assignments/week02_assignments.md` — Assignment 3.

        ## Interview Questions
        See `../../interview-prep/week02_ml_questions.md` — Section: Regression.

        ## Industry Use Cases
        - Demand forecasting, pricing models, risk scoring (credit/insurance)
        - Anomaly detection via residuals (actual - predicted)

        ## Common Mistakes
        - Not scaling features before Ridge/Lasso (penalty applies unevenly across scales)
        - Interpreting R^2 alone without checking residual patterns
        - Using linear regression for clearly non-linear relationships

        ## Best Practices
        - Always scale features before regularized regression
        - Check residual plots for non-linearity / heteroscedasticity
        - Start simple (linear) before reaching for complex models
        """
    )
    return


if __name__ == "__main__":
    app.run()
