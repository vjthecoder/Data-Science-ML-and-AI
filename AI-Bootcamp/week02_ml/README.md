# Week 2: Machine Learning Basics & ML Workflow

## Learning Objectives
- Frame business problems as ML problems
- Perform exploratory data analysis (EDA) and feature engineering
- Train/evaluate regression, classification, and clustering models
- Apply cross-validation and hyperparameter tuning correctly

## Estimated Duration
20-25 hours

## Prerequisites
- Week 1 (Python, NumPy, Pandas, Matplotlib/Seaborn)
- Basic statistics (mean, variance, distributions)

## Lesson Plan
See [`LESSON_PLAN.md`](LESSON_PLAN.md) for the day-by-day schedule.

## Diagrams
See [`../diagrams/week02_ml/`](../diagrams/week02_ml/README.md)

## Datasets
- `../resources/datasets/leads.csv`
- `../resources/datasets/churn.csv`
- `../resources/datasets/marketing_response.csv`
- `../resources/datasets/customers.csv` (from Week 1, used for clustering)

## Modules
1. Problem Framing — supervised vs unsupervised, business -> ML mapping
2. Exploratory Data Analysis (EDA)
3. Feature Engineering — encoding, scaling, missing values
4. Train/Test Split & Data Leakage
5. Regression — Linear, Ridge, Lasso
6. Classification — Logistic Regression, Decision Trees, Random Forest, XGBoost
7. Clustering — K-Means, Hierarchical
8. Evaluation Metrics — RMSE, MAE, Accuracy, Precision/Recall, F1, ROC-AUC, Silhouette
9. Cross Validation & Hyperparameter Tuning — GridSearchCV, RandomizedSearchCV

## Theory Notes
See `notebooks/` — each notebook explains theory at three levels with diagrams,
simple toy examples, and real datasets.

## Marimo Notebooks
Run any notebook with: `marimo edit week02_ml/notebooks/<file>.py`

- `notebooks/01_problem_framing_eda.py`
- `notebooks/02_feature_engineering.py`
- `notebooks/03_regression.py`
- `notebooks/04_classification.py`
- `notebooks/05_clustering.py`
- `notebooks/06_evaluation_metrics.py`
- `notebooks/07_cross_validation_tuning.py`

## Coding Labs
- `labs/lab1_lead_scoring.py` — Classification model to score sales leads
- `labs/lab2_customer_churn.py` — Predict customer churn
- `labs/lab3_marketing_response.py` — Predict response to marketing campaign

## Mini Projects
- Lead Scoring Model (end-to-end pipeline)
- Customer Churn Prediction (with tuned XGBoost)
- Marketing Response Prediction (with cross-validation)

## Real Industry Examples
- Sales: lead scoring to prioritize outreach
- Telecom/SaaS: churn prediction to trigger retention campaigns
- Marketing: response modeling to target high-propensity customers

## Assignments
See `assignments/`

## Interview Questions
See `../interview-prep/week02_ml_questions.md`

## Common Mistakes
- Fitting scalers/encoders on the full dataset before splitting (data leakage)
- Using accuracy on imbalanced datasets
- Not stratifying train/test splits for classification
- Overfitting via excessive hyperparameter search without held-out validation

## Best Practices
- Build pipelines with `sklearn.pipeline.Pipeline`
- Always split data before any fitting (scalers, encoders, imputers)
- Use stratified k-fold for classification
- Track experiments (metrics, params) for reproducibility

## Further Reading
- "Hands-On Machine Learning" by Aurélien Géron
- scikit-learn user guide
- XGBoost documentation
