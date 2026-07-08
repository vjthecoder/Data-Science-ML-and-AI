# Week 2 Interview Questions: Machine Learning Basics & ML Workflow

## Problem Framing & EDA
1. How do you decide whether a business problem is a classification, regression, or
   clustering problem?
2. What is data leakage? Give an example involving a time-based feature.
3. Why is checking class balance important before choosing a model and metric?
4. What questions would you ask a stakeholder before starting a churn prediction project?

## Feature Engineering
5. Why must you fit scalers/encoders on the training set only?
6. What's the difference between one-hot encoding and ordinal encoding? When would each be
   appropriate?
7. How would you handle a categorical feature with 10,000 unique values (high cardinality)?
8. What is the purpose of `ColumnTransformer` and `Pipeline` in scikit-learn?
9. Name three strategies for handling missing numeric data, and a trade-off for each.

## Regression
10. Explain the difference between Ridge and Lasso regression mathematically and practically.
11. What does R^2 measure, and what are its limitations?
12. When would RMSE and MAE give very different impressions of model quality?
13. What is multicollinearity, and how does it affect linear regression coefficients?

## Classification
14. Explain how a decision tree decides where to split (Gini impurity / information gain).
15. What is the difference between bagging (Random Forest) and boosting (XGBoost)?
16. Why might Logistic Regression be preferred over XGBoost in a regulated industry?
17. How does XGBoost handle missing values internally?
18. What is `class_weight="balanced"` and when would you use it?

## Clustering
19. How does K-Means choose initial centroids, and why does this matter (`n_init`)?
20. What is the elbow method, and what is the silhouette score? How do they complement each
    other?
21. Why is feature scaling critical for K-Means but less critical for tree-based models?
22. What's a real-world limitation of K-Means (hint: cluster shapes)?

## Evaluation Metrics
23. Walk through precision, recall, and F1 using a confusion matrix example.
24. When would you prioritize recall over precision? Give a concrete example.
25. What does ROC-AUC measure, and why is it threshold-independent?
26. Why is accuracy a poor metric for a dataset with 95% negative class?
27. How would you choose a classification threshold for a production system?

## Cross-Validation & Hyperparameter Tuning
28. Why is K-Fold cross-validation more reliable than a single train/test split?
29. What is the difference between `GridSearchCV` and `RandomizedSearchCV`? When would you
    use each?
30. Why should the final test set never be touched during hyperparameter tuning?
31. What is `StratifiedKFold`, and why is it preferred for classification with imbalanced
    classes?

## Scenario / System Design
32. You're asked to build a churn model for a telecom company. Walk through your end-to-end
    approach from problem framing to deployment.
33. Your model has 95% accuracy but the business says it's "useless" — what might be going
    wrong, and how would you diagnose it?
34. How would you monitor a deployed classification model for performance degradation over
    time (data drift / concept drift)?
35. A colleague's cross-validation score is much higher than their test score. What are
    possible causes, and how would you investigate?
