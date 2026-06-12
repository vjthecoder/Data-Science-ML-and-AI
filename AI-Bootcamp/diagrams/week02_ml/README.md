# Week 2 Diagrams: Machine Learning Basics & ML Workflow

## 1. ML Workflow Overview

```mermaid
flowchart LR
    A[Business Question] --> B[Problem Framing]
    B --> C[EDA]
    C --> D[Feature Engineering]
    D --> E[Train/Test Split]
    E --> F[Model Training]
    F --> G[Cross-Validation + Tuning]
    G --> H[Final Evaluation on Test Set]
    H --> I[Deployment / Report]
```

## 2. Leakage-Free Preprocessing

```mermaid
flowchart TD
    A[Raw Data] --> B[Train/Test Split]
    B --> C[Fit Scaler/Encoder on TRAIN only]
    C --> D[Transform TRAIN]
    C --> E[Transform TEST]
    D --> F[Fit Model]
    F --> G[Evaluate on Transformed TEST]
```

## 3. Bias-Variance / Model Family Spectrum

```mermaid
flowchart LR
    A[Logistic Regression\nHigh bias, low variance\nInterpretable] --> B[Decision Tree\nLow bias, high variance]
    B --> C[Random Forest\nBagging reduces variance]
    C --> D[XGBoost\nBoosting reduces bias\nState-of-the-art tabular]
```

## 4. Confusion Matrix & Metrics

```mermaid
flowchart TD
    CM["Confusion Matrix\nTN | FP\nFN | TP"] --> P["Precision = TP/(TP+FP)"]
    CM --> R["Recall = TP/(TP+FN)"]
    P --> F1["F1 = 2PR/(P+R)"]
    R --> F1
    CM --> ACC["Accuracy = (TP+TN)/Total"]
```

## 5. K-Fold Cross-Validation

```mermaid
flowchart TD
    D[Training Data] --> S1[Fold 1: Test | Train Train Train Train]
    D --> S2[Fold 2: Train Test Train Train Train]
    D --> S3[Fold 3: Train Train Test Train Train]
    D --> S4[Fold 4: Train Train Train Test Train]
    D --> S5[Fold 5: Train Train Train Train Test]
    S1 --> AVG[Average +/- Std across 5 scores]
    S2 --> AVG
    S3 --> AVG
    S4 --> AVG
    S5 --> AVG
```

## 6. Hyperparameter Tuning Flow

```mermaid
flowchart LR
    A[Define param grid] --> B[GridSearchCV / RandomizedSearchCV]
    B --> C[For each combo: K-Fold CV score]
    C --> D[Select best params]
    D --> E[Refit on full training set]
    E --> F[Evaluate once on held-out test set]
```
