import marimo

__generated_with = "0.9.0"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    import matplotlib.pyplot as plt
    import pandas as pd
    import seaborn as sns
    return mo, pd, plt, sns


@app.cell
def __(mo):
    mo.md(
        r"""
        # Lab 3: Marketing Campaign Analytics

        **Goal:** Analyze marketing campaign performance from
        `resources/datasets/marketing_campaigns.csv` and recommend where to allocate budget.

        ## Tasks
        1. Load data; compute CTR (clicks/impressions), conversion rate (conversions/clicks),
           CPA (spend/conversions), and ROAS (revenue/spend) per campaign.
        2. Aggregate metrics by `channel`.
        3. Visualize ROAS by channel.
        4. Recommend a budget reallocation.
        """
    )
    return


@app.cell
def __(pd):
    mkt = pd.read_csv("../../resources/datasets/marketing_campaigns.csv")
    mkt.head()
    return (mkt,)


@app.cell
def __(mkt, pd):
    mkt["ctr"] = mkt["clicks"] / mkt["impressions"]
    mkt["conversion_rate"] = mkt["conversions"] / mkt["clicks"]
    mkt["cpa"] = mkt["spend"] / mkt["conversions"].replace(0, pd.NA)
    mkt["roas"] = mkt["revenue"] / mkt["spend"]
    mkt[["campaign_id", "channel", "ctr", "conversion_rate", "cpa", "roas"]].head()
    return


@app.cell
def __(mkt):
    channel_summary = mkt.groupby("channel").agg(
        impressions=("impressions", "sum"),
        clicks=("clicks", "sum"),
        conversions=("conversions", "sum"),
        spend=("spend", "sum"),
        revenue=("revenue", "sum"),
    )
    channel_summary["ctr"] = (channel_summary["clicks"] / channel_summary["impressions"]).round(4)
    channel_summary["conversion_rate"] = (channel_summary["conversions"] / channel_summary["clicks"]).round(4)
    channel_summary["roas"] = (channel_summary["revenue"] / channel_summary["spend"]).round(2)
    channel_summary = channel_summary.sort_values("roas", ascending=False)
    channel_summary
    return (channel_summary,)


@app.cell
def __(channel_summary, plt, sns):
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(x=channel_summary.index, y=channel_summary["roas"], ax=ax, palette="mako")
    ax.axhline(1.0, color="red", linestyle="--", label="Break-even (ROAS=1)")
    ax.set_title("ROAS by Channel")
    ax.set_ylabel("Return on Ad Spend")
    ax.legend()
    fig
    return ax, fig


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Recommendation Template

        - Channel with highest ROAS: **___** -> recommend increasing budget allocation.
        - Channel(s) with ROAS < 1 (losing money): **___** -> recommend pausing or
          re-testing creative/targeting.
        - Channel with highest CTR but low conversion rate: **___** -> investigate landing
          page experience.

        ## Stretch Goal
        Compute a "budget reallocation" scenario: shift 20% of spend from the lowest-ROAS
        channel to the highest-ROAS channel, and re-estimate total revenue assuming ROAS
        stays constant.
        """
    )
    return


if __name__ == "__main__":
    app.run()
