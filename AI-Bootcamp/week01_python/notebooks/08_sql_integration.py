import marimo

__generated_with = "0.9.0"
app = marimo.App(width="medium")


@app.cell
def __():
    import sqlite3

    import marimo as mo
    import pandas as pd
    return mo, pd, sqlite3


@app.cell
def __(mo):
    mo.md(
        r"""
        # 08. SQL Integration with Python

        ## Theory

        **Level 1 (10-year-old):** A database is a giant, organized filing cabinet. SQL is the
        language you use to ask the cabinet questions, like "show me all the red folders from
        2024."

        **Level 2 (College Student):** SQL (Structured Query Language) is used to query relational
        databases via `SELECT`, `WHERE`, `GROUP BY`, `JOIN`, etc. Python's built-in `sqlite3` module
        lets you create/query a lightweight file-based database. `pandas.read_sql` runs a SQL
        query and returns a DataFrame directly.

        **Level 3 (Industry Professional):** Most production systems use SQL databases
        (PostgreSQL, MySQL, Snowflake, BigQuery) as the source of truth. Data scientists pull data
        via parameterized queries (never string-concatenate user input — SQL injection risk),
        often through an ORM (SQLAlchemy) or `read_sql` with connection objects.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Visual Explanation

        ```
        Python  --- SQL query (SELECT ...) --->  SQLite/Postgres DB
        Python  <--- rows of results -----------  SQLite/Postgres DB

        pd.read_sql("SELECT * FROM customers WHERE plan='Pro'", conn)
        -> returns a DataFrame
        ```
        """
    )
    return


@app.cell
def __(pd, sqlite3):
    # Simple Example: create an in-memory SQLite DB and load customers.csv into it
    conn = sqlite3.connect(":memory:")
    customers = pd.read_csv("../../resources/datasets/customers.csv")
    customers.to_sql("customers", conn, index=False, if_exists="replace")

    result = pd.read_sql("SELECT * FROM customers LIMIT 5", conn)
    result
    return conn, customers, result


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Real-World Example: Business Report via SQL

        A finance analyst needs: "average monthly spend per plan, for active customers only,
        ordered by spend descending" — written as SQL and executed from Python.
        """
    )
    return


@app.cell
def __(conn, pd):
    query = """
        SELECT plan, ROUND(AVG(monthly_spend), 2) AS avg_spend, COUNT(*) AS n_customers
        FROM customers
        WHERE is_active = 1
        GROUP BY plan
        ORDER BY avg_spend DESC
    """
    report = pd.read_sql(query, conn)
    report
    return query, report


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Parameterized Queries (Avoiding SQL Injection)

        **Never** do this with user input: `f"SELECT * FROM customers WHERE city = '{city}'"`.
        Always use parameter placeholders.
        """
    )
    return


@app.cell
def __(conn, pd):
    def customers_in_city(city: str):
        # Safe: parameterized query
        return pd.read_sql(
            "SELECT customer_id, name, city, monthly_spend FROM customers WHERE city = ?",
            conn,
            params=(city,),
        )

    customers_in_city("Mumbai").head()
    return (customers_in_city,)


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Coding Exercise

        1. Write a SQL query that returns the top 5 customers by `monthly_spend`.
        2. Write a SQL query that counts customers per `city`, ordered descending by count.
        3. Use a parameterized query to find all customers with `monthly_spend` greater than a
           given threshold (function `customers_above(conn, threshold)`).
        """
    )
    return


@app.cell
def __(conn, pd):
    top5 = pd.read_sql(
        "SELECT name, city, monthly_spend FROM customers ORDER BY monthly_spend DESC LIMIT 5",
        conn,
    )

    city_counts = pd.read_sql(
        "SELECT city, COUNT(*) AS n FROM customers GROUP BY city ORDER BY n DESC",
        conn,
    )

    def customers_above(connection, threshold: float):
        return pd.read_sql(
            "SELECT name, monthly_spend FROM customers WHERE monthly_spend > ? ORDER BY monthly_spend DESC",
            connection,
            params=(threshold,),
        )

    print(top5)
    print(city_counts)
    print(customers_above(conn, 300).head())
    return city_counts, customers_above, top5


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Assignment
        See `../assignments/week01_assignments.md` — Assignment 8.

        ## Interview Questions
        See `../../interview-prep/week01_python_questions.md` — Section: SQL Integration.

        ## Industry Use Cases
        - Pulling training data for ML models from a data warehouse
        - Daily/weekly business reports generated via scheduled SQL + Python jobs
        - Backend services querying application databases

        ## Common Mistakes
        - String-formatting SQL queries with user input (SQL injection)
        - Not closing database connections
        - Pulling entire tables into memory instead of filtering in SQL

        ## Best Practices
        - Always use parameterized queries
        - Push filtering/aggregation to the database when possible (faster, less memory)
        - Use context managers (`with sqlite3.connect(...) as conn:`) for connections
        """
    )
    return


if __name__ == "__main__":
    app.run()
