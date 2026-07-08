# Pandas Cheat Sheet

```python
import pandas as pd
```

## Load / inspect
```python
df = pd.read_csv("data.csv")          # read_json, read_sql, read_excel
df.head()  df.tail()  df.sample(5)
df.shape   df.dtypes   df.info()      # rows/cols, types, memory
df.describe()                          # numeric summary
df.isna().sum()                        # missing values per column
```

## Select
```python
df["col"]                 # a Series
df[["a", "b"]]            # a DataFrame
df.loc[rows, cols]        # label-based
df.iloc[0:5, 0:2]         # position-based
df.loc[df["age"] > 30]    # boolean filter
df.query("age > 30 and city == 'Pune'")
```

## Clean
```python
df = df.dropna(subset=["a"])          # drop rows missing 'a'
df["a"] = df["a"].fillna(df["a"].median())
df["date"] = pd.to_datetime(df["date"])
df = df.drop_duplicates()
df = df.rename(columns={"old": "new"})
df["cat"] = df["cat"].astype("category")   # save memory
```

## Transform
```python
df["annual"] = df["monthly"] * 12          # vectorized (preferred)
df["tier"] = df["spend"].apply(lambda x: "H" if x > 200 else "L")
df["norm"] = (df["x"] - df["x"].mean()) / df["x"].std()
df["copy"] = df.copy()                      # avoid SettingWithCopyWarning
```

## Group & aggregate
```python
df.groupby("city")["spend"].mean()
df.groupby(["city", "plan"]).agg(
    avg=("spend", "mean"), n=("id", "count")
).reset_index()
pd.pivot_table(df, values="rev", index="region", columns="cat", aggfunc="sum")
```

## Combine
```python
pd.concat([df1, df2])                        # stack rows
df1.merge(df2, on="id", how="left")          # SQL-style join
```

## Output
```python
df.to_csv("out.csv", index=False)
df.to_json("out.json", orient="records", indent=2)
```

## Gotchas
- Prefer vectorized ops over `.apply` with Python functions on large data.
- Use `.loc`/`.iloc` (not chained `df[...][...]`) to avoid `SettingWithCopyWarning`.
- `groupby(...).agg(...)` then `.reset_index()` to get a flat DataFrame back.
- `axis=0` = down columns; `axis=1` = across rows.
