# Datasets

All datasets here are **synthetically generated** for educational use (no real personal data).
Generated via seeded `random`/`numpy` scripts for reproducibility.

| File | Rows | Description | Used By |
|------|------|-------------|---------|
| `customers.csv` | 200 | Synthetic customer profiles (plan, spend, city, activity) | Week 1 notebooks 05, 08; Lab 1 |
| `sales.csv` | 500 | Synthetic order-level sales transactions | Week 1 notebooks 06; Labs 2, 3 (via aggregation) |
| `marketing_campaigns.csv` | 100 | Synthetic ad campaign performance metrics | Week 1 Lab 3 |
| `ab_test.csv` | 2000 | Synthetic A/B test results (control vs treatment) | Week 1 Lab 4 |

## License
All synthetic datasets in this folder are released under the same license as this
repository (MIT) — free to use, modify, and redistribute for learning purposes.

## Adding a New Dataset
1. Add the file here (prefer CSV, keep under 5MB).
2. Add a row to the table above: rows, description, which notebooks/labs use it.
3. If derived from a real-world source, document the source URL and its license.
