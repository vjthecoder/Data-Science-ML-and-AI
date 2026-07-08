import marimo

__generated_with = "0.9.0"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    return (mo,)


@app.cell
def __(mo):
    mo.md(
        r"""
        # 02. Control Flow — Loops & Conditionals

        ## Theory

        **Level 1 (10-year-old):** `if` is like a fork in the road — "if it's raining, take an
        umbrella; otherwise, don't." A loop is doing the same chore over and over, like brushing
        each tooth one by one.

        **Level 2 (College Student):** Conditionals (`if`/`elif`/`else`) branch execution based on
        boolean expressions. Loops (`for`, `while`) repeat a block of code. `for` iterates over
        an iterable (list, range, dict, file); `while` repeats until a condition becomes false.

        **Level 3 (Industry Professional):** Prefer vectorized operations (NumPy/Pandas) over
        Python-level loops for performance on large datasets — a Python `for` loop over a million
        rows is orders of magnitude slower than a vectorized NumPy operation due to interpreter
        overhead. Loops are still essential for I/O, orchestration, and control logic.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Visual Explanation

        ```
        for item in [10, 20, 30]:
            process(item)

        Iteration 1: item = 10 -> process(10)
        Iteration 2: item = 20 -> process(20)
        Iteration 3: item = 30 -> process(30)
        ```

        ```
        if condition:        # branch A
            ...
        elif other_condition: # branch B
            ...
        else:                 # branch C
            ...
        ```
        Only ONE branch executes per run.
        """
    )
    return


@app.cell
def __():
    # Simple Example: classify temperatures
    temps = [15, 22, 31, 5, 40]
    for t in temps:
        if t < 10:
            label = "Cold"
        elif t < 25:
            label = "Mild"
        else:
            label = "Hot"
        print(f"{t}°C -> {label}")
    return label, t, temps


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Real-World Example

        An e-commerce system applies discount tiers based on order value:

        - Order < ₹500: no discount
        - ₹500 <= Order < ₹2000: 5% discount
        - Order >= ₹2000: 10% discount

        This is implemented with `if`/`elif`/`else`, looped over every order in a batch file.
        """
    )
    return


@app.cell
def __():
    orders = [299, 750, 2200, 1999, 50]
    discounted = []
    for amount in orders:
        if amount >= 2000:
            discount = 0.10
        elif amount >= 500:
            discount = 0.05
        else:
            discount = 0.0
        final = round(amount * (1 - discount), 2)
        discounted.append(final)

    print(list(zip(orders, discounted)))

    # while loop example: simulate retrying an API call
    attempts = 0
    success = False
    while attempts < 3 and not success:
        attempts += 1
        success = attempts == 2  # pretend it succeeds on 2nd try
        print(f"Attempt {attempts}: success={success}")
    return amount, attempts, discount, discounted, final, orders, success


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Coding Exercise

        Given a list of exam scores `[45, 78, 92, 60, 33, 88]`:
        1. Loop through the scores.
        2. Assign a grade: `>=90` -> "A", `>=75` -> "B", `>=50` -> "C", else "F".
        3. Count how many students passed (grade != "F").
        """
    )
    return


@app.cell
def __():
    scores = [45, 78, 92, 60, 33, 88]
    passed = 0
    for score in scores:
        if score >= 90:
            grade = "A"
        elif score >= 75:
            grade = "B"
        elif score >= 50:
            grade = "C"
        else:
            grade = "F"
        if grade != "F":
            passed += 1
        print(score, "->", grade)
    print("Passed:", passed, "/", len(scores))
    return grade, passed, score, scores


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Assignment
        See `../assignments/week01_assignments.md` — Assignment 2.

        ## Interview Questions
        See `../../interview-prep/week01_python_questions.md` — Section: Control Flow.

        ## Industry Use Cases
        - Business rule engines (discount tiers, eligibility checks)
        - Retry logic for flaky network/API calls
        - Data validation loops before loading into a database

        ## Common Mistakes
        - Off-by-one errors with `range()`
        - Infinite `while` loops from forgetting to update the loop variable
        - Using `==` to compare floats (use tolerance instead)

        ## Best Practices
        - Use `enumerate()` instead of manual index counters
        - Prefer list comprehensions for simple transforms
        - Use `break`/`continue` sparingly and document why
        """
    )
    return


if __name__ == "__main__":
    app.run()
