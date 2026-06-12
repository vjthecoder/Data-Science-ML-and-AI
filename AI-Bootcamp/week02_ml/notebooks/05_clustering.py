import marimo

__generated_with = "0.9.0"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    import pandas as pd
    import matplotlib.pyplot as plt
    from sklearn.preprocessing import StandardScaler
    from sklearn.cluster import KMeans, AgglomerativeClustering
    from sklearn.metrics import silhouette_score
    return AgglomerativeClustering, KMeans, StandardScaler, mo, pd, plt, silhouette_score


@app.cell
def __(mo):
    mo.md(
        r"""
        # 05. Clustering — K-Means & Hierarchical

        ## Theory

        **Level 1 (10-year-old):** Clustering is like sorting a pile of mixed candy into groups
        by how similar they look — nobody tells you the groups in advance, you find them
        yourself.

        **Level 2 (College Student):** Clustering is unsupervised learning — no target labels.
        K-Means partitions data into `k` clusters by minimizing within-cluster variance
        (iteratively assigning points to the nearest centroid, then recomputing centroids).
        Hierarchical (Agglomerative) clustering builds a tree of nested clusters by repeatedly
        merging the closest pairs.

        **Level 3 (Industry Professional):** Clustering is widely used for customer
        segmentation, anomaly detection, and as a preprocessing step for other tasks. Choosing
        `k` is non-trivial — use the elbow method (inertia vs k) and silhouette score together.
        ALWAYS scale features before distance-based clustering, since K-Means uses Euclidean
        distance and unscaled features dominate.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Visual Explanation

        ```
        K-Means (k=3):

           *  *           Cluster A (centroid: x)
          *  x*

                  *  *     Cluster B (centroid: x)
                 * x *

        *    *             Cluster C (centroid: x)
         * x*

        Elbow method: plot inertia vs k, pick k where the curve "bends"
        ```
        """
    )
    return


@app.cell
def __(pd):
    df = pd.read_csv("../../resources/datasets/customers.csv")
    df.head()
    return (df,)


@app.cell
def __(KMeans, StandardScaler, df, plt):
    features = df[["age", "monthly_spend"]]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(features)

    inertias = []
    ks = range(1, 8)
    for k in ks:
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        km.fit(X_scaled)
        inertias.append(km.inertia_)

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(list(ks), inertias, marker="o")
    ax.set_xlabel("k")
    ax.set_ylabel("Inertia")
    ax.set_title("Elbow Method")
    fig
    return X_scaled, ax, fig, features, inertias, k, km, ks, scaler


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Real-World Example: Customer Segmentation (k=3)

        A marketing team segments customers by `age` and `monthly_spend` into 3 groups to
        target with different campaigns (e.g., "young high spenders", "budget-conscious",
        "older high spenders").
        """
    )
    return


@app.cell
def __(KMeans, X_scaled, df, plt, silhouette_score):
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    df["cluster"] = kmeans.fit_predict(X_scaled)

    sil = silhouette_score(X_scaled, df["cluster"])
    print("Silhouette score:", round(sil, 3))
    print(df.groupby("cluster")[["age", "monthly_spend"]].mean().round(1))

    fig2, ax2 = plt.subplots(figsize=(6, 5))
    scatter = ax2.scatter(df["age"], df["monthly_spend"], c=df["cluster"], cmap="viridis")
    ax2.set_xlabel("Age")
    ax2.set_ylabel("Monthly Spend")
    ax2.set_title("Customer Segments (K-Means, k=3)")
    fig2
    return ax2, fig2, kmeans, scatter, sil


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Coding Exercise

        1. Apply `AgglomerativeClustering` with `n_clusters=3` to the same scaled features.
        2. Compute its silhouette score and compare to K-Means.
        3. Try clustering on `["age", "monthly_spend", "is_active"]` (3 features) — does the
           silhouette score improve or worsen? Why might that be?
        """
    )
    return


@app.cell
def __(AgglomerativeClustering, StandardScaler, df, silhouette_score):
    agg = AgglomerativeClustering(n_clusters=3)
    X3 = df[["age", "monthly_spend", "is_active"]]
    X3_scaled = StandardScaler().fit_transform(X3)
    agg_labels = agg.fit_predict(X3_scaled)
    print("Agglomerative silhouette (3 features):", round(silhouette_score(X3_scaled, agg_labels), 3))
    return X3, X3_scaled, agg, agg_labels


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Assignment
        See `../assignments/week02_assignments.md` — Assignment 5.

        ## Interview Questions
        See `../../interview-prep/week02_ml_questions.md` — Section: Clustering.

        ## Industry Use Cases
        - Customer segmentation for marketing
        - Anomaly/outlier detection (points far from any cluster centroid)
        - Document/topic clustering (often on embeddings — preview of Week 3-4)

        ## Common Mistakes
        - Not scaling features before K-Means
        - Picking `k` arbitrarily without elbow/silhouette analysis
        - Interpreting cluster labels as having inherent meaning/order

        ## Best Practices
        - Always scale features for distance-based clustering
        - Use multiple metrics (elbow + silhouette) to choose `k`
        - Profile each cluster's feature means to give clusters business meaning
        """
    )
    return


if __name__ == "__main__":
    app.run()
