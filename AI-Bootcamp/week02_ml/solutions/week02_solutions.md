# Week 2 Solutions

Reference solutions for `../assignments/week02_assignments.md`. Try the assignments yourself
first.

---

## Solution 1 — Problem Framing & EDA

```python
import pandas as pd
mkt = pd.read_csv("resources/datasets/marketing_response.csv")

# Target: "responded" (0/1) -> binary classification
print("Response rate:", mkt["responded"].mean())
print(mkt.groupby("channel_preference")["responded"].mean())
```
**Leakage discussion:** `email_engagement_score` is plausible as a PRE-CAMPAIGN feature
(historical engagement), so it's likely safe — but if it were computed FROM the campaign
being predicted (e.g., "did they open THIS email"), it would leak the target. Always confirm
the feature's timestamp relative to the prediction point.

---

## Solution 2 — Feature Engineering

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

leads = pd.read_csv("resources/datasets/leads.csv")
leads["high_engagement"] = ((leads["website_visits"] > 10) | (leads["emails_opened"] > 5)).astype(int)

X = leads.drop(columns=["lead_id", "converted"])
y = leads["converted"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

preprocess = ColumnTransformer([
    ("num", StandardScaler(), ["website_visits", "emails_opened", "demo_requested", "high_engagement"]),
    ("cat", OneHotEncoder(handle_unknown="ignore"), ["source", "company_size", "industry", "budget_range"]),
])
X_train_t = preprocess.fit_transform(X_train)
X_test_t = preprocess.transform(X_test)
print(X_train_t.shape, X_test_t.shape)
print(preprocess.named_transformers_["cat"].categories_)
```

---

## Solution 3 — Regression

```python
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

sales = pd.read_csv("resources/datasets/sales.csv")
X = sales[["units", "unit_price", "category"]]
y = sales["revenue"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

preprocess = ColumnTransformer([
    ("cat", OneHotEncoder(handle_unknown="ignore"), ["category"]),
], remainder="passthrough")

for name, reg in [("Linear", LinearRegression()), ("Ridge", Ridge(alpha=1.0)), ("Lasso", Lasso(alpha=0.1))]:
    pipe = Pipeline([("prep", preprocess), ("reg", reg)])
    pipe.fit(X_train, y_train)
    preds = pipe.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, preds))
    mae = mean_absolute_error(y_test, preds)
    r2 = r2_score(y_test, preds)
    print(f"{name}: RMSE={rmse:.2f}, MAE={mae:.2f}, R2={r2:.4f}")
```
Since `revenue = units * unit_price` exactly (no noise), all models should fit near-perfectly
once `units` and `unit_price` are present (R^2 ~ 1 for non-regularized; Lasso may slightly
shrink `category` coefficients toward zero since they add little once `units`/`unit_price`
are included).

---

## Solution 4 — Classification

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

df = pd.read_csv("resources/datasets/churn.csv")
X = df.drop(columns=["customer_id", "churned"])
y = df["churned"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

preprocess = ColumnTransformer([
    ("num", StandardScaler(), ["tenure_months", "monthly_charges", "support_tickets"]),
    ("cat", OneHotEncoder(handle_unknown="ignore"), ["contract_type", "plan"]),
])

for name, clf in [("LogReg", LogisticRegression(max_iter=1000)), ("RandomForest", RandomForestClassifier(random_state=42))]:
    pipe = Pipeline([("prep", preprocess), ("model", clf)])
    pipe.fit(X_train, y_train)
    preds = pipe.predict(X_test)
    proba = pipe.predict_proba(X_test)[:, 1]
    print(name, accuracy_score(y_test, preds), precision_score(y_test, preds),
          recall_score(y_test, preds), f1_score(y_test, preds), roc_auc_score(y_test, proba))
```
**Recommendation:** If interpretability/regulatory needs dominate, choose Logistic
Regression (clear coefficients). If raw predictive performance matters most and the model
can be explained via SHAP, Random Forest is typically stronger on ROC-AUC.

---

## Solution 5 — Clustering

```python
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

df = pd.read_csv("resources/datasets/customers.csv")
X = StandardScaler().fit_transform(df[["age", "monthly_spend"]])

inertias, sils = [], []
for k in [2, 3, 4, 5]:
    km = KMeans(n_clusters=k, random_state=42, n_init=10).fit(X)
    inertias.append(km.inertia_)
    sils.append(silhouette_score(X, km.labels_))

print(list(zip([2,3,4,5], inertias, sils)))

best_k = 3  # pick based on elbow + silhouette
km = KMeans(n_clusters=best_k, random_state=42, n_init=10).fit(X)
df["cluster"] = km.labels_
print(df.groupby("cluster")[["age", "monthly_spend"]].mean())
```

---

## Solution 6 — Evaluation Metrics

```python
import numpy as np
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

# Using y_test, y_proba from the churn model in Assignment 4
cm = confusion_matrix(y_test, (y_proba >= 0.5).astype(int))
ConfusionMatrixDisplay(cm).plot()

best_t = None
for t in np.arange(0.05, 0.95, 0.01):
    preds_t = (y_proba >= t).astype(int)
    p = precision_score(y_test, preds_t, zero_division=0)
    r = recall_score(y_test, preds_t, zero_division=0)
    if p >= 0.5:
        best_t = t  # keep updating; lower thresholds generally raise recall
print("Lowest threshold with precision>=0.5:", best_t)
```
Lowering the threshold flags MORE customers as "at risk" — increases recall (catch more
churners) but also increases false positives, raising the retention team's workload.

---

## Solution 7 — Cross-Validation & Hyperparameter Tuning

```python
import pandas as pd
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score, GridSearchCV
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score

leads = pd.read_csv("resources/datasets/leads.csv")
X = leads.drop(columns=["lead_id", "converted"])
y = leads["converted"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

preprocess = ColumnTransformer([
    ("num", StandardScaler(), ["website_visits", "emails_opened", "demo_requested"]),
    ("cat", OneHotEncoder(handle_unknown="ignore"), ["source", "company_size", "industry", "budget_range"]),
])
pipe = Pipeline([("prep", preprocess), ("model", RandomForestClassifier(random_state=42))])
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

base_scores = cross_val_score(pipe, X_train, y_train, cv=cv, scoring="f1")
print("Baseline CV F1:", base_scores.mean())

grid = GridSearchCV(pipe, {"model__n_estimators": [50, 100, 200], "model__max_depth": [3, 5, None]}, cv=cv, scoring="f1", n_jobs=-1)
grid.fit(X_train, y_train)
print("Best params:", grid.best_params_, "Best CV F1:", grid.best_score_)

test_f1 = f1_score(y_test, grid.best_estimator_.predict(X_test))
print("Test F1:", test_f1)
```
A large gap between CV F1 and test F1 would suggest overfitting to the validation folds
during tuning, or that the test set distribution differs from training data.
