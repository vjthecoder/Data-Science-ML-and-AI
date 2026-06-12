# Week 1: Python for Data Science & AI

## Learning Objectives
- Write clean, idiomatic Python (variables, data types, loops, functions, OOP)
- Manipulate data with NumPy and Pandas
- Visualize data with Matplotlib and Seaborn
- Consume REST APIs and parse JSON
- Query data from SQL databases using Python

## Estimated Duration
20-25 hours (1 week, part-time)

## Prerequisites
- None — absolute beginner friendly
- A computer with Python 3.10+ and Jupyter installed

## Modules
1. Python Fundamentals — Variables, Data Types, Operators
2. Control Flow — Loops, Conditionals
3. Functions & OOP — Functions, Classes, Objects, Inheritance
4. NumPy — Arrays, Vectorized Operations
5. Pandas — DataFrames, Cleaning, Aggregation
6. Matplotlib & Seaborn — Static & Statistical Visualization
7. APIs & JSON — Requests, Parsing, Auth
8. SQL Integration — sqlite3, pandas.read_sql

## Theory Notes
See `notebooks/01_python_fundamentals.ipynb` through `notebooks/08_sql_integration.ipynb`
for theory explained at three levels (10-year-old / college student / industry professional),
with visual explanations, simple examples, and real-world examples.

## Jupyter Notebooks
- `notebooks/01_python_fundamentals.ipynb`
- `notebooks/02_control_flow.ipynb`
- `notebooks/03_functions_oop.ipynb`
- `notebooks/04_numpy.ipynb`
- `notebooks/05_pandas.ipynb`
- `notebooks/06_matplotlib_seaborn.ipynb`
- `notebooks/07_apis_json.ipynb`
- `notebooks/08_sql_integration.ipynb`

## Coding Labs
- `labs/lab1_customer_data_analysis.ipynb` — Clean & analyze a customer dataset with Pandas
- `labs/lab2_sales_dashboard.ipynb` — Build a sales dashboard with Matplotlib/Seaborn
- `labs/lab3_marketing_analytics.ipynb` — Marketing campaign analytics with Pandas
- `labs/lab4_ab_testing.ipynb` — A/B testing dataset analysis & statistical comparison

## Mini Projects
- Customer Data Analysis Report
- Sales Dashboard (multi-chart)
- Marketing Campaign Performance Analysis
- A/B Test Result Summary

## Real Industry Examples
- E-commerce: customer segmentation from transaction logs
- SaaS: churn signals from usage data pulled via API
- Marketing: campaign ROI dashboards from CSV exports
- Product: A/B test significance testing for feature rollouts

## Assignments
See `assignments/` for weekly assignment set.

## Interview Questions
See `../interview-prep/week01_python_questions.md`

## Common Mistakes
- Using loops instead of vectorized NumPy/Pandas operations
- Mutating lists/dicts while iterating over them
- Ignoring `SettingWithCopyWarning` in Pandas
- Hardcoding API keys instead of using environment variables
- Not closing database connections

## Best Practices
- Prefer vectorized operations over explicit Python loops
- Use virtual environments and `.env` files for secrets
- Write small, single-purpose functions with type hints
- Use `df.copy()` when creating derived DataFrames
- Always validate API responses before parsing

## Further Reading
- "Python for Data Analysis" by Wes McKinney
- NumPy & Pandas official documentation
- Real Python tutorials on OOP and APIs
