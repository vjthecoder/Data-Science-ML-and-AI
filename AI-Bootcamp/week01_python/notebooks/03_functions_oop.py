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
        # 03. Functions & Object-Oriented Programming

        ## Theory

        **Level 1 (10-year-old):** A function is like a recipe — you give it ingredients (inputs),
        it does the cooking, and gives you a dish (output). A class is like a cookie cutter — you
        use it to stamp out many cookies (objects) that all have the same shape but can have
        different decorations (data).

        **Level 2 (College Student):** Functions are reusable blocks of code that take parameters
        and return values. Classes bundle data (attributes) and behavior (methods) together.
        `__init__` is the constructor. Inheritance lets a subclass reuse and extend a parent
        class's behavior.

        **Level 3 (Industry Professional):** Functions should be small, pure where possible (no
        side effects), and have clear type signatures. OOP is used for modeling entities with
        state + behavior (e.g., a `Model` class wrapping a trained ML model with `.predict()`,
        `.save()`, `.load()`). Favor composition over deep inheritance hierarchies; use
        dataclasses or Pydantic models for structured data.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Visual Explanation

        ```
        def add(a, b):      <- function definition
            return a + b

        result = add(3, 4)  <- function call -> result = 7
        ```

        ```
        class Customer:                  # blueprint
            def __init__(self, name, spend):
                self.name = name
                self.spend = spend

            def is_high_value(self):
                return self.spend > 100

        c1 = Customer("Alice", 250)   # object 1
        c2 = Customer("Bob", 40)      # object 2
        ```
        """
    )
    return


@app.cell
def __():
    # Simple Example: functions
    def add(a: float, b: float) -> float:
        """Return the sum of two numbers."""
        return a + b

    def discount_price(price: float, pct: float) -> float:
        """Apply a percentage discount to a price."""
        return round(price * (1 - pct / 100), 2)

    print(add(3, 4))
    print(discount_price(1000, 15))
    return add, discount_price


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Real-World Example

        A retail analytics team models each `Customer` as a class with attributes (name, total
        spend, signup date) and methods (`is_high_value()`, `lifetime_value()`). This is far
        cleaner than passing around loose dictionaries everywhere, and methods centralize
        business logic (e.g., the definition of "high value" lives in ONE place).
        """
    )
    return


@app.cell
def __():
    class Customer:
        """Represents a customer with spend-based segmentation."""

        def __init__(self, name: str, monthly_spend: float, months_active: int):
            self.name = name
            self.monthly_spend = monthly_spend
            self.months_active = months_active

        def lifetime_value(self) -> float:
            return self.monthly_spend * self.months_active

        def is_high_value(self, threshold: float = 100.0) -> bool:
            return self.monthly_spend > threshold

        def __repr__(self) -> str:
            return f"Customer(name={self.name!r}, ltv={self.lifetime_value():.2f})"


    class EnterpriseCustomer(Customer):
        """A Customer subclass with an account manager (inheritance example)."""

        def __init__(self, name, monthly_spend, months_active, account_manager):
            super().__init__(name, monthly_spend, months_active)
            self.account_manager = account_manager

        def is_high_value(self, threshold: float = 100.0) -> bool:
            return True  # all enterprise customers are high value


    customers = [
        Customer("Alice", 250, 6),
        Customer("Bob", 40, 3),
        EnterpriseCustomer("Globex Corp", 80, 12, account_manager="Priya"),
    ]

    for cust in customers:
        print(cust, "| high value:", cust.is_high_value())
    return Customer, EnterpriseCustomer, customers, cust


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Coding Exercise

        1. Write a function `bmi(weight_kg, height_m) -> float` that returns BMI = weight / height^2.
        2. Create a class `Patient` with `name`, `weight_kg`, `height_m`, and a method
           `bmi_category()` returning "Underweight" (<18.5), "Normal" (18.5-24.9), "Overweight"
           (25-29.9), or "Obese" (>=30).
        """
    )
    return


@app.cell
def __():
    def bmi(weight_kg: float, height_m: float) -> float:
        return round(weight_kg / (height_m ** 2), 2)


    class Patient:
        def __init__(self, name: str, weight_kg: float, height_m: float):
            self.name = name
            self.weight_kg = weight_kg
            self.height_m = height_m

        def bmi_category(self) -> str:
            value = bmi(self.weight_kg, self.height_m)
            if value < 18.5:
                return "Underweight"
            elif value < 25:
                return "Normal"
            elif value < 30:
                return "Overweight"
            return "Obese"


    p = Patient("Ravi", 78, 1.75)
    print(bmi(p.weight_kg, p.height_m), p.bmi_category())
    return Patient, bmi, p


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Assignment
        See `../assignments/week01_assignments.md` — Assignment 3.

        ## Interview Questions
        See `../../interview-prep/week01_python_questions.md` — Section: Functions & OOP.

        ## Industry Use Cases
        - ML model wrapper classes (`.fit()`, `.predict()`, `.save()`)
        - ETL pipeline steps as small, testable functions
        - Domain models (Customer, Order, Invoice) in business applications

        ## Common Mistakes
        - Mutable default arguments (e.g., `def f(items=[])`)
        - God classes that do too much (violates single responsibility)
        - Overusing inheritance where composition is simpler

        ## Best Practices
        - Keep functions short and single-purpose; add docstrings and type hints
        - Use `@dataclass` for simple data containers
        - Favor composition over inheritance for flexibility
        """
    )
    return


if __name__ == "__main__":
    app.run()
