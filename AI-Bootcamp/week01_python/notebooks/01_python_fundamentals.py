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
        # 01. Python Fundamentals — Variables & Data Types

        ## Learning Objectives
        - Understand variables, data types, and operators in Python
        - Explain each concept at 3 levels: a 10-year-old, a college student, an industry professional

        ## Theory

        **Level 1 (10-year-old):** A variable is like a labeled box. You can put a number, a word,
        or a list of things inside the box, and give the box a name so you can find it again.

        **Level 2 (College Student):** A variable is a name bound to an object in memory. Python is
        dynamically typed — the same name can be rebound to objects of different types. Core built-in
        types: `int`, `float`, `str`, `bool`, `list`, `tuple`, `dict`, `set`, `NoneType`.

        **Level 3 (Industry Professional):** Variables are references to objects on the heap; Python
        uses reference counting + garbage collection for memory management. Type hints (`typing`
        module) don't change runtime behavior but enable static analysis (mypy, pyright) — critical
        in production codebases for catching bugs before deployment.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Visual Explanation

        ```
        name = "Alice"        age = 30          is_active = True
        ┌─────────┐          ┌─────────┐        ┌─────────┐
        │  name   │--------->│ "Alice" │        │  age    │----> 30
        └─────────┘          └─────────┘        └─────────┘
        ```
        Each variable name points to an object somewhere in memory. Reassigning a
        variable just points the label to a new object — it doesn't change the old one.
        """
    )
    return


@app.cell
def __():
    # Simple Example: basic data types
    name: str = "Alice"
    age: int = 30
    height_m: float = 1.65
    is_active: bool = True
    skills: list = ["Python", "SQL", "Excel"]
    profile: dict = {"name": name, "age": age, "skills": skills}

    print(type(name), type(age), type(height_m), type(is_active))
    print(profile)
    return age, height_m, is_active, name, profile, skills


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Real-World Example

        A SaaS company stores each user's signup info as a dictionary fetched from an API:

        ```python
        user = {
            "user_id": 10234,
            "email": "jane@example.com",
            "plan": "Pro",
            "monthly_spend": 49.99,
            "is_trial": False,
        }
        ```

        Every field has a distinct type (`int`, `str`, `float`, `bool`). Knowing types matters
        because `monthly_spend * 12` only works if `monthly_spend` is numeric — if the API
        returned `"49.99"` (a string), you'd need to convert it with `float()` first.
        """
    )
    return


@app.cell
def __():
    # Operators demo
    a, b = 17, 5
    print("Addition:", a + b)
    print("Floor division:", a // b)
    print("Modulo:", a % b)
    print("Exponent:", a ** 2)
    print("Comparison a > b:", a > b)
    print("Logical:", (a > 10) and (b < 10))

    # Common pitfall: string vs number from an API
    api_value = "49.99"
    annual_spend = float(api_value) * 12
    print("Annual spend:", annual_spend)
    return a, annual_spend, api_value, b


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Coding Exercise

        1. Create variables for a product: `product_name` (str), `price` (float), `quantity` (int),
           `in_stock` (bool).
        2. Compute `total_cost = price * quantity`.
        3. Print a formatted sentence using an f-string:
           `"<product_name>: <quantity> units at ₹<price> each = ₹<total_cost>"`
        """
    )
    return


@app.cell
def __():
    # TODO: Your solution here
    product_name = "Wireless Mouse"
    price = 799.0
    quantity = 3
    in_stock = True

    total_cost = price * quantity
    print(f"{product_name}: {quantity} units at ₹{price} each = ₹{total_cost}")
    return in_stock, price, product_name, quantity, total_cost


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Assignment
        See `../assignments/week01_assignments.md` — Assignment 1.

        ## Interview Questions
        See `../../interview-prep/week01_python_questions.md` — Section: Fundamentals.

        ## Industry Use Cases
        - Configuration objects (dicts) for ML pipelines
        - Type-safe API request/response models (Pydantic builds on these basics)
        - Feature flags represented as booleans

        ## Common Mistakes
        - Comparing types incorrectly (`"5" == 5` is `False`)
        - Forgetting that lists are mutable and shared by reference

        ## Best Practices
        - Use descriptive variable names (`monthly_spend`, not `ms`)
        - Add type hints for function signatures and complex variables
        """
    )
    return


if __name__ == "__main__":
    app.run()
