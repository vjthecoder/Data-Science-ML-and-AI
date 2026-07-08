# Week 1 Diagrams: Python for Data Science & AI

## 1. Data Analysis Pipeline (Pandas)

```mermaid
flowchart LR
    A[Raw CSV/JSON/SQL Data] --> B[Load into DataFrame]
    B --> C[Inspect: shape, dtypes, nulls]
    C --> D[Clean: handle missing values, fix dtypes]
    D --> E[Transform: new columns, filtering, grouping]
    E --> F[Visualize: Matplotlib/Seaborn]
    F --> G[Report / Dashboard]
```

## 2. API -> JSON -> DataFrame Flow

```mermaid
sequenceDiagram
    participant Py as Python Client
    participant API as REST API
    Py->>API: GET /resource (headers: API key)
    API-->>Py: 200 OK + JSON body
    Py->>Py: json.loads() -> dict/list
    Py->>Py: pd.DataFrame(data)
    Py->>Py: Analysis / Visualization
```

## 3. Control Flow: Discount Tier Logic

```mermaid
flowchart TD
    Start[Order Amount] --> Q1{Amount >= 2000?}
    Q1 -- Yes --> D1[10% Discount]
    Q1 -- No --> Q2{Amount >= 500?}
    Q2 -- Yes --> D2[5% Discount]
    Q2 -- No --> D3[No Discount]
    D1 --> End[Final Price]
    D2 --> End
    D3 --> End
```

## 4. Class Hierarchy Example (OOP)

```mermaid
classDiagram
    class Customer {
        +str name
        +float monthly_spend
        +int months_active
        +lifetime_value() float
        +is_high_value() bool
    }
    class EnterpriseCustomer {
        +str account_manager
        +is_high_value() bool
    }
    Customer <|-- EnterpriseCustomer
```

## 5. NumPy Broadcasting

```mermaid
flowchart LR
    A["Array shape (5,): [199, 499, 999, 49, 1499]"] --> C[Element-wise multiply + add]
    B["Scalars 1.07 and 10 broadcast to shape (5,)"] --> C
    C --> D["Result shape (5,): final_price"]
```

## 6. SQL Query Execution Flow

```mermaid
flowchart LR
    A[pandas DataFrame] -->|to_sql| B[(SQLite DB)]
    B -->|"SELECT ... GROUP BY ..."| C[Query Result Rows]
    C -->|read_sql| D[pandas DataFrame: Report]
```
