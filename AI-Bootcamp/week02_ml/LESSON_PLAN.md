# Week 2 Lesson Plan: Machine Learning Basics & ML Workflow

**Total Duration:** ~20-25 hours over 5-6 days

| Day | Topics | Notebook(s) | Duration | Deliverable |
|-----|--------|-------------|----------|-------------|
| 1 | Problem Framing & EDA | `01_problem_framing_eda.py` | 3h | Assignment 1 |
| 2 | Feature Engineering | `02_feature_engineering.py` | 3h | Assignment 2 |
| 3 | Regression + Classification | `03_regression.py`, `04_classification.py` | 5h | Assignments 3-4 |
| 4 | Clustering + Lab 1 (Lead Scoring) | `05_clustering.py`, `labs/lab1_lead_scoring.py` | 4h | Assignment 5, Lab 1 |
| 5 | Evaluation Metrics + Lab 2 (Churn) | `06_evaluation_metrics.py`, `labs/lab2_customer_churn.py` | 4h | Assignment 6, Lab 2 |
| 6 | Cross-Validation/Tuning + Lab 3 (Marketing Response) | `07_cross_validation_tuning.py`, `labs/lab3_marketing_response.py` | 4-5h | Assignment 7, Lab 3 |

## Session Format (per day)
Same as Week 1: warm-up review -> theory walkthrough (3 levels) -> live coding -> guided
exercise -> lab/assignment -> wrap-up (common mistakes + best practices).

## Prerequisites Check (Day 0)
```bash
pip install -r AI-Bootcamp/requirements.txt
# verify scikit-learn and xgboost import successfully
python -c "import sklearn, xgboost; print(sklearn.__version__, xgboost.__version__)"
```

## Assessment
- 7 assignments — see `assignments/week02_assignments.md`
- 3 labs (Lead Scoring, Customer Churn, Marketing Response) — see `labs/`
- End-of-week quiz drawn from `../interview-prep/week02_ml_questions.md`

## Success Criteria
By the end of Week 2, students can:
- Frame a business problem as a supervised/unsupervised ML task and identify leakage risks
- Build leakage-free preprocessing pipelines with `ColumnTransformer`/`Pipeline`
- Train and compare regression, classification, and clustering models
- Choose evaluation metrics aligned with business cost and interpret ROC/PR curves
- Use cross-validation and `GridSearchCV`/`RandomizedSearchCV` for robust model selection
