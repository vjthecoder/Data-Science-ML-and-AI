# Week 2 Assignments

Complete each assignment in a new Marimo notebook inside this folder, named
`assignment<N>_<your_name>.py`. Reference solutions are in `../solutions/`.

---

## Assignment 1 — Problem Framing & EDA

Using `resources/datasets/marketing_response.csv`:
1. State the ML framing: what is the target, and is it classification or regression?
2. Compute the response rate overall and by `channel_preference`.
3. Check for any features that might cause leakage if used at prediction time (consider:
   would `email_engagement_score` be known BEFORE sending the campaign?). Justify your answer.

---

## Assignment 2 — Feature Engineering

Using `resources/datasets/leads.csv`:
1. Create a feature `high_engagement` = 1 if `website_visits > 10` OR `emails_opened > 5`,
   else 0.
2. Build a `ColumnTransformer` that scales numeric features and one-hot encodes categorical
   features, fit ONLY on a training split.
3. Confirm no data leakage: print the shape of the transformed train and test sets and
   verify the encoder's learned categories come only from the training data.

---

## Assignment 3 — Regression

Using `resources/datasets/sales.csv`:
1. Predict `revenue` using `units`, `unit_price`, and one-hot encoded `category`.
2. Compare `LinearRegression`, `Ridge(alpha=1.0)`, and `Lasso(alpha=0.1)` on RMSE, MAE, R^2.
3. Which model performs best, and does Lasso zero out any coefficients? What does that imply
   about the `category` feature's usefulness?

---

## Assignment 4 — Classification

Using `resources/datasets/churn.csv`:
1. Build a pipeline with `LogisticRegression` and one with `RandomForestClassifier`.
2. Evaluate both on accuracy, precision, recall, F1, and ROC-AUC.
3. Which model would you recommend to the business, and why — consider both performance AND
   interpretability.

---

## Assignment 5 — Clustering

Using `resources/datasets/customers.csv`:
1. Cluster customers using K-Means on `["age", "monthly_spend"]` with `k=2, 3, 4, 5`.
2. Plot the elbow curve and silhouette scores for each `k`.
3. Pick the best `k` and describe each resulting cluster in 1 sentence (e.g., "Cluster 0:
   young, low spenders").

---

## Assignment 6 — Evaluation Metrics

Using your churn model from Assignment 4 (Random Forest):
1. Plot the confusion matrix at the default 0.5 threshold.
2. Find the threshold that maximizes recall while keeping precision >= 0.5.
3. Explain, in business terms, what changing the threshold would mean for the retention team's
   workload (more/fewer customers flagged for outreach).

---

## Assignment 7 — Cross-Validation & Hyperparameter Tuning

Using `resources/datasets/leads.csv`:
1. Run 5-fold `StratifiedKFold` cross-validation for a `RandomForestClassifier` (default
   params), scoring=`f1`.
2. Use `GridSearchCV` to tune `n_estimators` (50, 100, 200) and `max_depth` (3, 5, None).
3. Report the best parameters, best CV F1, and the final test-set F1. Is there a meaningful
   gap between CV score and test score? What would a large gap suggest?
