# Week 1 Interview Questions: Python for Data Science & AI

## Fundamentals (Variables & Data Types)
1. What is the difference between a list, a tuple, and a set in Python?
2. What does it mean that Python is "dynamically typed"? How does this differ from statically
   typed languages like Java?
3. Explain mutable vs. immutable types with examples. Why does this matter for function
   arguments?
4. What is the difference between `is` and `==`?
5. How would you convert a string `"49.99"` to a float, and what happens if the conversion fails?

## Control Flow
6. When would you use a `while` loop instead of a `for` loop?
7. What is the difference between `break`, `continue`, and `pass`?
8. Explain list comprehensions. Rewrite this loop as a comprehension:
   ```python
   result = []
   for x in range(10):
       if x % 2 == 0:
           result.append(x * x)
   ```
9. What is a common pitfall when looping over a list while modifying it?
10. How would you avoid an infinite `while` loop when polling an API for a result?

## Functions & OOP
11. What is the difference between a positional argument, a keyword argument, and `*args`/`**kwargs`?
12. Why is using a mutable default argument (e.g., `def f(items=[])`) considered a bug risk?
13. Explain `self` in Python classes. Why is it explicitly listed in method signatures?
14. What is the difference between `@staticmethod`, `@classmethod`, and a regular instance method?
15. Explain inheritance vs. composition. When would you prefer composition?
16. What is method overriding, and how does `super()` work?

## NumPy
17. Why is NumPy faster than pure Python loops for numerical operations?
18. What is broadcasting? Give an example where broadcasting fails.
19. What is the difference between `np.array.reshape()` and `np.array.flatten()`?
20. How would you select all elements of an array greater than a threshold?
21. What's the difference between a "view" and a "copy" in NumPy, and why does it matter?

## Pandas
22. What is the difference between `.loc[]` and `.iloc[]`?
23. Explain `groupby()`. What does `df.groupby("col").agg({"x": "mean", "y": "sum"})` do?
24. How do you handle missing data in Pandas? Name at least 3 strategies.
25. What causes `SettingWithCopyWarning`, and how do you avoid it?
26. What is the difference between `merge()`, `join()`, and `concat()`?
27. How would you find duplicate rows in a DataFrame and remove them?

## Visualization
28. When would you choose a bar chart vs. a histogram vs. a box plot?
29. What is the difference between Matplotlib and Seaborn? Why use both together?
30. How would you visualize the correlation between numeric columns in a DataFrame?
31. What makes a chart "misleading," and how can you avoid it?

## APIs & JSON
32. What is the difference between GET, POST, PUT, and DELETE HTTP methods?
33. How do you handle authentication when calling a third-party API (e.g., API keys, OAuth)?
34. What is the difference between `json.dumps()` and `json.loads()`?
35. How would you handle a nested JSON structure to extract a deeply nested field safely?
36. Why is it important to set a timeout on API requests, and what happens if you don't?

## SQL Integration
37. What is the difference between `INNER JOIN`, `LEFT JOIN`, and `FULL OUTER JOIN`?
38. What is SQL injection, and how do parameterized queries prevent it?
39. How would you use Python to run a SQL query and load the result directly into a DataFrame?
40. When should aggregation/filtering be done in SQL vs. in Pandas?

## Scenario / System Design
41. You're given a 5GB CSV file that doesn't fit comfortably in memory. How would you process it
    with Pandas?
42. Design a small Python script that: pulls data from an API every hour, stores it in SQLite,
    and generates a daily summary report. What components would you need?
43. A teammate's code uses nested loops to join two lists of dictionaries by ID. How would you
    refactor it to be more efficient and Pythonic?
