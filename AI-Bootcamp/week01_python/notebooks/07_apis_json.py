import marimo

__generated_with = "0.9.0"
app = marimo.App(width="medium")


@app.cell
def __():
    import json

    import marimo as mo
    return json, mo


@app.cell
def __(mo):
    mo.md(
        r"""
        # 07. APIs & JSON

        ## Theory

        **Level 1 (10-year-old):** An API is like ordering food through a menu — you ask for
        something specific (a request), and the kitchen (server) sends back your food (response).
        JSON is just a way of writing down information using `{ }` boxes and `[ ]` lists.

        **Level 2 (College Student):** REST APIs expose resources over HTTP using methods (GET,
        POST, PUT, DELETE). JSON (JavaScript Object Notation) is a lightweight text format for
        structured data — maps directly to Python dicts/lists via the `json` module. Authentication
        is commonly via API keys or OAuth bearer tokens in headers.

        **Level 3 (Industry Professional):** Production API clients need: timeout handling, retry
        with backoff, status code checks, rate-limit handling, and secret management (never hardcode
        keys — use environment variables / secret managers). Pydantic models are often used to
        validate and parse API responses into typed Python objects.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Visual Explanation

        ```
        Client (your code)              Server (API)
              |---- GET /users/123 ----------->|
              |                                 | (looks up user 123)
              |<---- 200 OK + JSON body --------|

        JSON body:
        {
          "id": 123,
          "name": "Alice",
          "skills": ["Python", "SQL"],
          "active": true
        }
        ```
        """
    )
    return


@app.cell
def __(json):
    # Simple Example: working with JSON strings (no network needed)
    json_text = '''
    {
        "id": 123,
        "name": "Alice",
        "skills": ["Python", "SQL", "Pandas"],
        "active": true,
        "address": {"city": "Mumbai", "zip": "400001"}
    }
    '''

    user = json.loads(json_text)  # JSON string -> Python dict
    print(type(user), user["name"], user["skills"], user["address"]["city"])

    # Python dict -> JSON string
    back_to_json = json.dumps(user, indent=2)
    print(back_to_json)
    return back_to_json, json_text, user


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Real-World Example: Calling a Public REST API

        We call the public JSONPlaceholder API to fetch a fake "user" resource and parse it
        into Python. (Requires internet access; falls back to a local mock if unavailable.)
        """
    )
    return


@app.cell
def __(json):
    import requests

    def fetch_user(user_id: int) -> dict:
        url = f"https://jsonplaceholder.typicode.com/users/{user_id}"
        try:
            resp = requests.get(url, timeout=5)
            resp.raise_for_status()
            return resp.json()
        except Exception as exc:
            print(f"API call failed ({exc}); using mock data instead.")
            return {"id": user_id, "name": "Mock User", "email": "mock@example.com",
                    "company": {"name": "Mock Co"}}

    data = fetch_user(1)
    print(json.dumps(data, indent=2)[:400])
    return data, fetch_user, requests


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Coding Exercise

        1. Write a function `extract_fields(user_json)` that returns a flat dict with keys
           `name`, `email`, and `company` (from `user_json["company"]["name"]`).
        2. Call it on the result from `fetch_user(1)` and print it.
        3. Bonus: write a function `safe_get(d, *keys, default=None)` that safely navigates
           nested dicts without raising `KeyError`.
        """
    )
    return


@app.cell
def __(data):
    def extract_fields(user_json: dict) -> dict:
        return {
            "name": user_json.get("name"),
            "email": user_json.get("email"),
            "company": user_json.get("company", {}).get("name"),
        }

    def safe_get(d: dict, *keys, default=None):
        for key in keys:
            if isinstance(d, dict) and key in d:
                d = d[key]
            else:
                return default
        return d

    print(extract_fields(data))
    print(safe_get(data, "company", "name"))
    print(safe_get(data, "company", "missing_key", default="N/A"))
    return extract_fields, safe_get


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Assignment
        See `../assignments/week01_assignments.md` — Assignment 7.

        ## Interview Questions
        See `../../interview-prep/week01_python_questions.md` — Section: APIs & JSON.

        ## Industry Use Cases
        - Pulling data from third-party services (payment, CRM, weather, LLM providers)
        - Webhooks: receiving JSON payloads on events
        - Microservices communicating via REST/JSON

        ## Common Mistakes
        - Not checking HTTP status codes before parsing the body
        - Hardcoding API keys in source code
        - Assuming a JSON field always exists (use `.get()` with defaults)

        ## Best Practices
        - Always set request timeouts
        - Store secrets in environment variables / `.env` files (never commit them)
        - Validate/parse responses with Pydantic models in production code
        """
    )
    return


if __name__ == "__main__":
    app.run()
