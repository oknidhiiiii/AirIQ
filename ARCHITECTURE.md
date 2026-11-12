# AirIQ System Architecture & System Blueprint
## AirIQ: Airbnb Pricing & Market Intelligence Using Apache PySpark

---

## 1. Architectural Overview

AirIQ follows a **layered, decoupled enterprise big data architecture** built around Apache PySpark. The pipeline isolates data ingestion, cleaning, analytics aggregation, feature engineering, machine learning modeling, intelligence inference, and presentation into modular execution boundaries.

```mermaid
flowchart TD
    subgraph Environment & Validation Layer
        E0[Spark Smoke Test: airiq.spark.smoke_test]
        A1[Raw CSV / GZ Listings Data]
        A2[Schema Specification StructType]
    end

    subgraph Ingestion & Processing Layer
        B1[SparkSession Local Master: local[8]]
        B2[Schema-Enforced Reader]
        B3[Data Hygiene Engine: Invalid Removal]
        B4[Outlier Flagging & Imputation]
    end

    subgraph Storage Layer
        C1[Cleaned Listings Parquet Store]
        C2[Analytics Aggregations Parquet Store]
        C3[ML Model Artifacts & Metrics JSON]
    end

    subgraph Analytics Layer
        D1[Spark SQL Engine]
        D2[Geospatial Pricing Module]
        D3[Host & Property Module]
        D4[Demand Proxy Module]
    end

    subgraph ML & Intelligence Layer
        E1[Leakage-Safe MLlib Feature Pipeline]
        E2[Regressors: Simple Baseline, LR, RF, GBT]
        E3[Inverse expm1 & USD Error Metrics]
        E4[Market Mispricing Tiers: Under/Overpriced]
    end

    subgraph Presentation Layer
        F1[Streamlit UI Core with OBSERVED vs PROXY Badges]
        F2[Interactive Plotly Dashboards]
        F3[Real-Time ML PipelineModel Predictor]
    end

    E0 -->|Pass Smoke Test| B1
    A1 -->|Raw Input| B2
    A2 -->|Validate Schema| B2
    B2 -->|Raw DataFrame| B3
    B3 -->|Cleaned DataFrame| B4
    B4 -->|Write Parquet| C1

    C1 -->|Read Parquet| D1
    D1 -->|SQL Aggregations| D2
    D1 -->|SQL Aggregations| D3
    D1 -->|SQL Aggregations| D4
    D2 & D3 & D4 -->|Write Parquet| C2

    C1 -->|Read Cleaned Data| E1
    E1 -->|Vector Assembler| E2
    E2 -->|Predictions| E3
    E3 -->|Under/Overpriced Tiers| E4
    E2 & E4 -->|Store Artifacts| C3

    C2 & C3 -->|Load Fast Views| F1
    F1 --> F2
    F1 --> F3
```

---

## 2. Layer-by-Layer Architectural Specification

### A. Environment & Validation Layer (`airiq.spark`)
- **Smoke Test Module:** `airiq.spark.smoke_test.py` executes prior to dataset ingestion to verify PySpark JVM startup, local cluster thread allocation (`local[8]`), and DataFrame creation.
- **Ingestion Schema:** `airiq.ingestion.schema.py` enforces explicit `StructType` schema definitions on raw CSV files.

### B. PySpark Data Processing & Hygiene Layer (`airiq.cleaning`)
- **Engine:** PySpark DataFrame API (`pyspark.sql.functions`).
- **Data Quality Segmentation:**
  - **Invalid Record Removal:** `price <= 0.0` or `accommodates < 1` filtered out.
  - **Statistical Outlier Flagging:** High-price listings retained for analysis; binary flag `is_high_price_outlier` added.
- **Target Transformation:** `log_price = log1p(price)`.
- **Null Imputation:** Neighborhood-level median imputation for missing rating sub-scores computed strictly during training.

### C. Analytical Query & Feature Store Layer (`airiq.analytics`)
- **Engine:** Spark SQL Engine (`spark.sql`) & Window Functions (`pyspark.sql.window.Window`).
- **Execution:** Runs 9 modular analytical queries covering geographic pricing, host tier dynamics, room type cross-tabulations, availability distribution, and demand proxies.
- **Persistence:** Aggregated summary tables are serialized to compressed Parquet format partitioned by `neighbourhood_group`.

### D. Machine Learning Pipeline Layer (`airiq.models`)
- **Engine:** PySpark MLlib (`pyspark.ml`).
- **Pipeline Architecture:**
  1. `StringIndexer`: Converts categorical strings (`room_type`, `neighbourhood_group_cleansed`) into numerical category indices.
  2. `OneHotEncoder`: Converts indices into binary sparse vectors.
  3. `VectorAssembler`: Combines sparse category vectors and continuous numerical features into a single unified `features` vector column.
  4. `Estimators`: Trains Simple Baseline, Linear Regression, Random Forest Regressor, and Gradient-Boosted Trees on `log1p(price)`.
- **Target Inversion & Metrics:** Evaluates predictions using $\text{expm1}(\hat{y})$ to calculate MAE, RMSE, and $R^2$ in USD currency units.

### E. Market Mispricing Intelligence Engine (`airiq.intelligence`)
- **Engine:** PySpark SQL math functions.
- **Logic:**
  - Computes raw residual: $e_i = price_i - \hat{price}_i$.
  - Calculates standardized residual Z-score: $Z_i = \frac{e_i - \bar{e}}{\sigma_e}$.
  - Classifies listings into mispricing categories: **Potentially Underpriced** ($Z < -1.0$), **Fair Market Value** ($-1.0 \le Z \le 1.0$), **Potentially Overpriced** ($Z > 1.0$).

### F. Presentation & Visualization Layer (`dashboard`)
- **Engine:** Streamlit + Plotly Express.
- **Observed vs Proxy Badge Protocol:** Explicit visual labels distinguish OBSERVED DATA (raw prices, room types, review counts) from DERIVED ESTIMATES / PROXIES (estimated monthly bookings, occupancy rate).
- **Inference Singleton Pattern:** Loads the trained PySpark `PipelineModel` into memory, transforms user form inputs via 1-row Spark DataFrames, and displays real-time predicted price in USD.

---

## 3. Spark Memory & Execution Model for Local Hardware

```
+-----------------------------------------------------------------------+
|                      Spark Driver & Local Executor                    |
|                        (AMD Ryzen 9 5900HS - 8 Cores / 16 Threads)    |
|                                                                       |
|  +-----------------------------+     +-----------------------------+  |
|  | Driver Memory: 4 GB         |     | Executor Memory: 4 GB       |  |
|  +-----------------------------+     +-----------------------------+  |
|  | Shuffle Partitions: 8       |     | PySpark Worker Threads: 8   |  |
|  +-----------------------------+     +-----------------------------+  |
+-----------------------------------------------------------------------+
```

### Local Cluster Configuration Parameters (`config/default_config.yaml`)
- `spark.master`: `local[8]`
- `spark.driver.memory`: `4g`
- `spark.executor.memory`: `4g`
- `spark.sql.shuffle.partitions`: `8`
- `spark.serializer`: `org.apache.spark.serializer.KryoSerializer`

---

## 4. Fault Tolerance, Error Handling & Logging Strategy

- **Centralized Logging:** `airiq.utils.logging_utils` provides structured logging across driver execution steps with timestamp, log level, and component tag.
- **Exception Boundary Handling:**
  - File IO errors (missing dataset file) raise explicit `FileNotFoundError` with user actionable downloading instructions.
  - Schema mismatches raise custom `SchemaValidationError`.
- **Graceful Spark Termination:** All entry points utilize Python context managers or `try...finally` blocks to guarantee `spark.stop()` execution, preventing orphaned JVM gateway processes.
