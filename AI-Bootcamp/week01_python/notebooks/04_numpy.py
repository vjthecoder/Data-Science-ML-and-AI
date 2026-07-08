import marimo

__generated_with = "0.9.0"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    import numpy as np
    return mo, np


@app.cell
def __(mo):
    mo.md(
        r"""
        # 04. NumPy — Arrays & Vectorized Operations

        ## Theory

        **Level 1 (10-year-old):** Imagine a giant egg carton where every slot holds a number, and
        you can do math to ALL the eggs at once — like adding 1 to every egg in one go, instead of
        picking each one up individually.

        **Level 2 (College Student):** NumPy's `ndarray` is a fixed-type, contiguous block of
        memory. Operations are "vectorized" — applied element-wise without explicit Python loops,
        implemented in C for speed. Broadcasting allows operations between arrays of different
        shapes under specific rules.

        **Level 3 (Industry Professional):** NumPy is the foundation of the entire PyData stack
        (Pandas, scikit-learn, PyTorch tensors share similar memory semantics). Vectorization
        avoids Python's per-element interpreter overhead — typically 10-100x faster than pure
        Python loops. Understanding broadcasting and `dtype` is essential for memory-efficient,
        bug-free numerical code.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Visual Explanation

        ```
        Python list loop:           NumPy vectorized:
        for x in data:              result = data * 2
            result.append(x*2)      (single C-level operation over the whole array)

        Broadcasting:
        [1, 2, 3]  (shape (3,))
              +
            10      (scalar, broadcast to shape (3,))
              =
        [11, 12, 13]
        ```
        """
    )
    return


@app.cell
def __(np):
    # Simple Example
    arr = np.array([1, 2, 3, 4, 5])
    print("Array:", arr)
    print("Mean:", arr.mean())
    print("Sum:", arr.sum())
    print("Squared:", arr ** 2)
    print("Boolean mask (>2):", arr > 2)
    print("Filtered:", arr[arr > 2])

    matrix = np.arange(1, 13).reshape(3, 4)
    print("\nMatrix:\n", matrix)
    print("Column sums:", matrix.sum(axis=0))
    print("Row means:", matrix.mean(axis=1))
    return arr, matrix


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Real-World Example

        A pricing team has unit prices for 10,000 products and wants to apply a 7% GST and a
        flat ₹10 shipping fee to all of them. With NumPy:

        ```python
        final_price = prices * 1.07 + 10
        ```

        This single vectorized line replaces a 10,000-iteration Python loop and runs near
        C-speed.
        """
    )
    return


@app.cell
def __(np):
    prices = np.array([199.0, 499.0, 999.0, 49.0, 1499.0])
    final_price = prices * 1.07 + 10
    print(final_price)

    # Random data + statistics (useful for simulations / A-B testing)
    rng = np.random.default_rng(42)
    sample = rng.normal(loc=100, scale=15, size=1000)
    print("\nSample mean:", round(sample.mean(), 2))
    print("Sample std:", round(sample.std(), 2))
    print("95th percentile:", round(np.percentile(sample, 95), 2))
    return final_price, prices, rng, sample


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Coding Exercise

        Given an array of daily website visitors for 30 days (use
        `np.random.default_rng(1).integers(100, 1000, size=30)`):
        1. Compute the mean, max, and min visitors.
        2. Find how many days had more than 500 visitors.
        3. Normalize the array to a 0-1 range: `(x - min) / (max - min)`.
        """
    )
    return


@app.cell
def __(np):
    visitors = np.random.default_rng(1).integers(100, 1000, size=30)
    print("Mean:", visitors.mean())
    print("Max:", visitors.max(), "Min:", visitors.min())
    print("Days > 500:", (visitors > 500).sum())

    normalized = (visitors - visitors.min()) / (visitors.max() - visitors.min())
    print("Normalized sample:", normalized[:5])
    return normalized, visitors


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Assignment
        See `../assignments/week01_assignments.md` — Assignment 4.

        ## Interview Questions
        See `../../interview-prep/week01_python_questions.md` — Section: NumPy.

        ## Industry Use Cases
        - Feature scaling/normalization before model training
        - Vectorized financial calculations (pricing, interest)
        - Image data represented as multi-dimensional arrays

        ## Common Mistakes
        - Mixing `dtype`s causing unexpected upcasting
        - Using Python loops over NumPy arrays (defeats the purpose)
        - Confusing `axis=0` (columns) vs `axis=1` (rows) in aggregations

        ## Best Practices
        - Always vectorize when possible
        - Use `np.where` for conditional element-wise logic
        - Set a random seed (`default_rng(seed)`) for reproducibility
        """
    )
    return


if __name__ == "__main__":
    app.run()
