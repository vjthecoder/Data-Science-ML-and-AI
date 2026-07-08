import marimo

__generated_with = "0.9.0"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    import seaborn as sns
    return mo, np, pd, plt, sns


@app.cell
def __(mo):
    mo.md(
        r"""
        # Lab 4: A/B Testing Dataset Analysis

        **Goal:** Analyze an A/B test (`resources/datasets/ab_test.csv`) comparing a `control`
        and `treatment` group on conversion rate and time on page.

        ## Tasks
        1. Load data; compute conversion rate and average time-on-page per group.
        2. Visualize the difference.
        3. Run a two-proportion z-test for conversion rate difference.
        4. Conclude whether the treatment is statistically significantly better.
        """
    )
    return


@app.cell
def __(pd):
    ab = pd.read_csv("../../resources/datasets/ab_test.csv")
    ab.head()
    return (ab,)


@app.cell
def __(ab):
    summary = ab.groupby("group").agg(
        users=("user_id", "count"),
        conversions=("converted", "sum"),
        avg_time_on_page=("time_on_page_sec", "mean"),
    )
    summary["conversion_rate"] = (summary["conversions"] / summary["users"]).round(4)
    summary
    return (summary,)


@app.cell
def __(ab, plt, sns):
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    conv_rate = ab.groupby("group")["converted"].mean()
    sns.barplot(x=conv_rate.index, y=conv_rate.values, ax=axes[0], palette="Set2")
    axes[0].set_title("Conversion Rate by Group")
    axes[0].set_ylabel("Conversion Rate")

    sns.boxplot(x="group", y="time_on_page_sec", data=ab, ax=axes[1], palette="Set2")
    axes[1].set_title("Time on Page by Group")
    fig.tight_layout()
    fig
    return axes, conv_rate, fig


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Statistical Significance: Two-Proportion Z-Test

        $$ z = \frac{\hat{p}_1 - \hat{p}_2}{\sqrt{\hat{p}(1-\hat{p})\left(\frac{1}{n_1}+\frac{1}{n_2}\right)}} $$

        where $\hat{p}$ is the pooled conversion rate. A $|z| > 1.96$ corresponds roughly to
        a p-value < 0.05 (95% confidence).
        """
    )
    return


@app.cell
def __(ab, np):
    control = ab[ab["group"] == "control"]
    treatment = ab[ab["group"] == "treatment"]

    n1, n2 = len(control), len(treatment)
    x1, x2 = control["converted"].sum(), treatment["converted"].sum()
    p1, p2 = x1 / n1, x2 / n2

    p_pool = (x1 + x2) / (n1 + n2)
    se = np.sqrt(p_pool * (1 - p_pool) * (1 / n1 + 1 / n2))
    z_score = (p2 - p1) / se

    print(f"Control conversion rate:   {p1:.4f} (n={n1})")
    print(f"Treatment conversion rate: {p2:.4f} (n={n2})")
    print(f"Z-score: {z_score:.3f}")
    print("Significant at 95%?" , abs(z_score) > 1.96)
    return control, n1, n2, p1, p2, p_pool, se, treatment, x1, x2, z_score


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Conclusion Template

        - Treatment conversion rate is **___%** vs control's **___%**, a relative lift of **___%**.
        - The z-score of **___** (is / is not) statistically significant at the 95% level.
        - Recommendation: (ship the treatment / keep testing / roll back) because ___.

        ## Stretch Goal
        Compute a 95% confidence interval for the difference in conversion rates:
        $(\hat{p}_2 - \hat{p}_1) \pm 1.96 \times SE$
        """
    )
    return


if __name__ == "__main__":
    app.run()
