# AirIQ: Airbnb Pricing & Market Intelligence Using Apache PySpark
## Comprehensive Project Plan & Implementation Blueprint

---

## 1. Project Title
**AirIQ: Airbnb Pricing & Market Intelligence Using Apache PySpark**

---

## 2. Abstract
AirIQ is an enterprise-grade big data analytics and machine learning system engineered to process, analyze, and model short-term rental market dynamics at scale using **Apache PySpark**. By leveraging distributed PySpark DataFrames, Spark SQL, and PySpark MLlib, AirIQ addresses key challenges faced by property hosts, real estate investors, and market analysts: understanding price determinants, evaluating spatial and property-type pricing dynamics, quantifying demand proxies, and detecting market mispricing (overpriced and underpriced listings). The system processes large-scale granular listing data, applies rigorous data hygiene and feature engineering pipelines, trains scalable regression models, and exposes interactive insights via a lightweight Streamlit analytics dashboard backed by optimized Parquet storage.

---

## 3. Problem Statement
The short-term rental market is characterized by extreme heterogeneity across pricing, property configurations, host behaviors, geographic locations, and guest demand. Property hosts often struggle with dynamic pricing strategies, leading to either sub-optimal revenue (underpricing) or low occupancy (overpricing). 

Conventional single-node tools (e.g., pandas, Excel) fail to scale efficiently when processing multi-gigabyte or multi-million record rental datasets with complex nested attributes, text features, and multi-year historical reviews. Furthermore, naïve analytical approaches often conflate review counts or availability with direct booking records. 

AirIQ solves these problems by providing:
1. A scalable, distributed big data processing pipeline built on **PySpark**.
2. A rigorous analytical framework distinguishing empirical **demand proxy metrics** from direct transaction logs.
3. A PySpark MLlib pricing model capable of predicting market listing prices ($\exp(\hat{y}) - 1$) and identifying listings that deviate significantly from expected market value.

---

## 4. Motivation
1. **Academic & Engineering Rigor:** Demonstrating end-to-end Big Data Analytics (BDA) practices—from raw schema enforcement and distributed cleaning to Spark SQL analytics, MLlib pipelines, and production visualization.
2. **Market Transparency:** Enabling hosts to price listings competitively based on objective listing characteristics (location, amenities, room type, capacity) and review feedback.
3. **Scalable Architecture:** Creating a blueprint that runs efficiently on a single multi-core workstation/laptop (`local[8]`) while remaining seamlessly deployable to multi-node Spark clusters (YARN, Kubernetes, Databricks).

---

## 5. Project Objectives
1. **Distributed Data Processing:** Construct a PySpark data ingestion pipeline capable of reading, parsing, and cleaning multi-thousand/million row rental datasets with strict `StructType` schema validation.
2. **Data Hygiene & Preprocessing:** Implement distributed data quality transformations, handling invalid records (negative prices, zero capacity), applying conditional median imputation, and maintaining statistical outliers for analytical inspection.
3. **Exploratory Market Analytics:** Execute multi-dimensional market analysis (geographic, host tier, property type, rating distribution, and demand proxies) utilizing **Spark SQL** and window functions.
4. **Demand Proxy Modeling:** Formalize and calculate empirical demand proxies (such as review rates and estimated occupancy via the San Francisco Model: $Estimated\_Bookings = \frac{reviews\_per\_month}{0.50}$) while maintaining clear conceptual distinctions from direct booking transaction logs.
5. **Distributed Machine Learning:** Build, train, and evaluate scalable regression models using **PySpark MLlib** (Simple Mean Baseline, Linear Regression, Random Forest Regressor, and Gradient-Boosted Trees) to predict `log1p(price)`.
6. **Market Mispricing Detection Engine:** Design a statistical residual analysis pipeline ($e_i = price_i - \hat{price}_i$) to flag listings as **Potentially Underpriced**, **Fair Market Value**, or **Potentially Overpriced**.
7. **Interactive Intelligence Dashboard:** Develop a Streamlit dashboard that queries pre-computed, partitioned Parquet outputs to deliver responsive UI visual analytics with explicit visual separation between OBSERVED DATA and DERIVED ESTIMATES / PROXIES.
8. **Reproducibility & Quality Assurance:** Ensure full reproducibility through strict environment pinning (Python 3.14.7 + OpenJDK 21 + PySpark 3.5.1), automated Spark smoke testing, deterministic random seeds, unit test coverage with `pytest`, and comprehensive technical documentation.

---

## 6. Dataset Requirements & Verification

### Live Verified Dataset Sourcing
- **Data Source:** Inside Airbnb Open Data Portal (http://insideairbnb.com/get-the-data/)
- **Live Verified URL:** `https://data.insideairbnb.com/united-states/ny/new-york-city/2026-06-14/data/listings.csv.gz`
- **Configurable Fallback:** Supported via `config/default_config.yaml` to handle URL updates gracefully.
- **HTTP Status:** 200 OK (Verified via HTTP response headers)
- **File Format:** Compressed CSV (`listings.csv.gz`), ~15.7 MB compressed / ~100 MB+ raw uncompressed.
- **Row Count & Attributes:** ~38,000+ detailed listing records with 75 schema attributes.
- **Licensing:** Creative Commons Attribution 4.0 International (CC BY 4.0).

---

## 7. Dataset Evaluation: Booking Proxy Metrics vs. Actual Booking Data

> [!IMPORTANT]
> **Mandatory Academic & Analytical Integrity Rule:**
> Public Inside Airbnb datasets consist of **point-in-time listing snapshots** and historical review metrics. They **DO NOT** contain private host transaction records, exact calendar booking IDs, or dollar revenue receipts.
> 
> In this project:
> - **Actual Booking Data:** Refers strictly to verified transaction logs (unavailable in public datasets).
> - **Demand Proxy Metrics:** Refers to calculated demand indicators grounded in industry standard research (e.g., **San Francisco Model**: $Estimated\_Bookings = \frac{reviews\_per\_month}{0.50}$).
> 
> The project strictly labels all demand-related charts and metrics as **Demand Proxies** across all UI tabs, reports, and code modules.

---

## 8. Functional Requirements
1. **Spark Smoke Test Module:** Pre-pipeline verification script (`airiq/spark/smoke_test.py`) ensuring PySpark JVM initialization and basic DataFrame operations function cleanly before pipeline execution.
2. **Data Ingestion Module:** Read raw CSV/CSV.GZ data into PySpark using an explicitly defined `StructType` schema.
3. **Cleaning & Transformation Module:** Clean currency formats, filter invalid records (`price <= 0`, `accommodates < 1`), handle missing ratings via conditional median imputation, compute `log_price = log1p(price)`, and add statistical outlier indicator flags.
4. **Analytics Core Module:** Execute 9 distinct analytical modules utilizing Spark SQL aggregations, windowing functions, and statistical summaries.
5. **PySpark MLlib Modeling Module:** 
   - Assemble features via `VectorAssembler`, `StringIndexer`, and `OneHotEncoder`.
   - Perform train/test split (80/20 ratio) with fixed random seeds.
   - Train Baseline Simple Mean Model, Linear Regression, Random Forest Regressor, and Gradient-Boosted Trees (GBT).
   - Evaluate predictions on original currency scale using `expm1(predicted_log_price)` to compute MAE, RMSE, and $R^2$.
6. **Price Intelligence Engine:** Calculate residuals ($e = price - \hat{price}$) and classify listings into residual Z-score tiers: Underpriced ($Z < -1.0$), Fair Market Value ($-1.0 \le Z \le 1.0$), and Overpriced ($Z > 1.0$).
7. **Dashboard & Visualization Interface:** Provide an interactive Streamlit UI rendering multi-tab visual insights powered by pre-aggregated Parquet data outputs, featuring an interactive listing price predictor utilizing the trained PySpark ML PipelineModel.

---

## 9. Non-Functional Requirements
1. **Performance:** Pipeline execution must complete within 2–4 minutes on the target student machine (AMD Ryzen 9 5900HS 16 threads, 15 GB RAM) using `local[8]`.
2. **Scalability:** Code structure must use PySpark DataFrame APIs natively, avoiding single-node bottlenecks (`collect()`, Python UDFs) so it can scale to multi-node clusters without modification.
3. **Reproducibility:** Single-command setup and execution (`python -m airiq.cli run-all`) producing deterministic, repeatable ML model metrics.
4. **Code Quality & Modular Architecture:** Clear separation of concerns into modular packages (`config`, `ingestion`, `cleaning`, `analytics`, `models`, `dashboard`, `utils`).
5. **Fault Tolerance & Logging:** Comprehensive logging using standard Python/Spark logging frameworks with explicit error handling for missing files or invalid schemas.

---

## 10. Outlier Strategy: Invalid Records vs. Statistical Outliers

AirIQ enforces a clear, documented distinction between invalid data entries and valid statistical market extremes:

### A. Invalid Records (Removed / Corrected)
- Negative or zero listing prices (`price <= 0.0`)
- Impossible room/capacity counts (`accommodates < 1`)
- Malformed geospatial coordinates (`latitude` or `longitude` outside valid NYC bounding box)
- Unparseable date strings in essential fields (`host_since`)

### B. Statistical Outliers (Retained & Analyzed)
- Luxury high-price listings (e.g. `$1,500 - $5,000+` per night)
- High review count listings (e.g. `number_of_reviews > 300`)
- High availability listings (`availability_365 = 365`)

Statistical outliers are preserved in the main analytical and training datasets to allow AirIQ to model high-end market dynamics. Binary indicator flags (e.g., `is_high_price_outlier = when(price > Q3 + 1.5*IQR, 1).otherwise(0)`) are added for downstream segment filtering.

---

## 11. Machine Learning Plan & Data Leakage Prevention

### Pipeline Sequence (Leakage-Safe)
```
Raw Data
   ↓
Basic Deterministic Cleaning (Invalid record removal, regex price parsing)
   ↓
Train / Test Split (80% Train, 20% Test, Seed = 42)
   ↓
Training-Only Learned Preprocessing (Compute category maps, impute values strictly on Train split)
   ↓
Feature Pipeline Assembly (StringIndexer, OneHotEncoder, VectorAssembler)
   ↓
Model Training (Simple Baseline, Linear Regression, Random Forest, GBT)
   ↓
Test Dataset Transformation (Apply fitted PipelineModel to Test split)
   ↓
Inverse Target Transformation (expm1(predicted_log_price))
   ↓
Evaluation Metrics Calculation (Original USD Scale MAE, RMSE, R² & Log-scale metrics)
```

### Evaluated Models
1. **Simple Baseline Model:** Predicts train set target mean/median for all test samples.
2. **Linear Regression (`LinearRegression`):** Standard linear model with elastic-net regularization.
3. **Random Forest Regressor (`RandomForestRegressor`):** Non-linear ensemble (`numTrees=100`, `maxDepth=8`).
4. **Gradient-Boosted Trees (`GBTRegressor`):** Iterative boosting model (`maxIter=50`, `maxDepth=6`).

---

## 12. Dashboard Inference Architecture

The Streamlit dashboard (`dashboard/app.py`) does not require an active multi-node cluster or continuous batch background job execution:

```
[User Input Form] 
       │
       ▼
[Construct 1-Row Spark DataFrame via Cached SparkSession]
       │
       ▼
[Load Pre-Trained PySpark ML PipelineModel]
       │
       ▼
[PipelineModel.transform(input_df)] ──► [Predicted log1p(price)]
       │
       ▼
[expm1 Transformation] ──► [Display Real-Time Predicted USD Price]
```

To manage SparkSession lifecycle safely in Streamlit, AirIQ wraps `SparkSession` instantiation in a `@st.cache_resource` singleton function, preventing thread leakages or JVM crashes across UI re-renders.

---

## 13. Project Directory Structure

```
AirIQ/
├── PROJECT_PLAN.md
├── ARCHITECTURE.md
├── DATA_DICTIONARY.md
├── METHODOLOGY.md
├── SETUP.md
├── TECHNICAL_DECISIONS.md
├── PRE_IMPLEMENTATION_REVIEW.md
├── requirements.txt
├── setup.py
├── config/
│   └── default_config.yaml
├── data/
│   ├── raw/
│   │   └── .gitkeep
│   ├── processed/
│   │   └── analytics/
│   └── outputs/
│       ├── models/
│       └── metrics/
├── src/
│   └── airiq/
│       ├── __init__.py
│       ├── cli.py
│       ├── spark/
│       │   ├── __init__.py
│       │   ├── session.py
│       │   └── smoke_test.py
│       ├── ingestion/
│       │   ├── __init__.py
│       │   ├── schema.py
│       │   └── reader.py
│       ├── cleaning/
│       │   ├── __init__.py
│       │   └── transformer.py
│       ├── analytics/
│       │   ├── __init__.py
│       │   ├── modules.py
│       │   └── sql_queries.py
│       ├── models/
│       │   ├── __init__.py
│       │   ├── pipeline.py
│       │   ├── trainer.py
│       │   └── evaluator.py
│       ├── intelligence/
│       │   ├── __init__.py
│       │   └── mispricing.py
│       └── utils/
│           ├── __init__.py
│           └── logging_utils.py
├── dashboard/
│   ├── app.py
│   └── components/
└── tests/
    ├── __init__.py
    ├── test_smoke.py
    ├── test_schema.py
    ├── test_cleaning.py
    ├── test_analytics.py
    └── test_ml_pipeline.py
```

---

## 14. Academic Viva Defense & Key Technical Explanations

1. **Q: Why Python 3.14 + OpenJDK 21 + PySpark 3.5.1?**  
   *Answer:* This environment combination was empirically tested and verified via a Spark smoke test (`airiq/spark/smoke_test.py`). PySpark 3.5.1 runs cleanly on Java 21 LTS JVM and Python 3.14.7 without bytecode or serialization errors.

2. **Q: How does `log1p` and `expm1` differ from standard `log` and `exp`?**  
   *Answer:* $\text{log1p}(x) = \ln(1 + x)$ and $\text{expm1}(x) = \exp(x) - 1$. Using `log1p` avoids numerical instability and mathematical errors ($\ln(0) = -\infty$) if listing price or feature values approach zero. `expm1` provides exact mathematical inversion back to currency units.

3. **Q: Why evaluate metrics on original USD scale instead of log-scale alone?**  
   *Answer:* While training minimizes log-scale error loss, stakeholders interpret pricing performance in dollars ($USD$). Reporting MAE and RMSE in dollars reveals the actual financial error magnitude of predictions, while log-scale metrics ($RMSE_{log}$) explain model loss optimization behavior.

4. **Q: How are statistical price outliers handled compared to invalid records?**  
   *Answer:* Invalid records (negative prices, zero capacity) represent data corruption and are removed. Statistical outliers (luxury penthouses, high availability listings) represent real market phenomena and are retained in training data, marked with binary indicator flags (`is_high_price_outlier`).

5. **Q: How is PySpark MLlib leakage avoided?**  
   *Answer:* All parameter fittings (median imputation statistics, StringIndexer category maps, VectorAssembler scalers) are computed strictly on the 80% train split inside a `pyspark.ml.Pipeline`. The fitted `PipelineModel` then transforms the test split without recalculating statistics.

6. **Q: How is demand modeled when booking transactions are unavailable?**  
   *Answer:* Demand is modeled strictly via empirical **Demand Proxies** using the academic San Francisco Model ($Estimated\_Bookings = \frac{reviews\_per\_month}{0.50}$). Derived estimates are explicitly labeled as proxies across all dashboard screens and documentation to preserve analytical integrity.
