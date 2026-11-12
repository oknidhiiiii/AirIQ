# AirIQ Technical Decisions & Architectural Rationale
## AirIQ: Airbnb Pricing & Market Intelligence Using Apache PySpark

---

## 1. Environment Compatibility & PySpark Engine Verification
- **Decision:** Use **Python 3.14.7**, **OpenJDK 21.0.12.1**, and **PySpark 3.5.1**.
- **Rationale:** While Python 3.14 and OpenJDK 21 are modern releases, we empirically validated compatibility by executing a PySpark smoke test (`local[2]` master session) before finalizing planning documents. PySpark 3.5.1 initialized without JVM bytecode errors, serialization conflicts, or gateway failures.
- **Enforcement:** A mandatory pre-flight smoke test script (`airiq/spark/smoke_test.py`) runs prior to pipeline execution.

---

## 2. Dataset Sourcing & Dynamic URL Resolution
- **Decision:** Source detailed listings from Inside Airbnb NYC dataset using configurable URL parameters in `config/default_config.yaml`.
- **Rationale:** Inside Airbnb updates dataset URL structures quarterly (e.g. `2026-06-14`). Hardcoding fixed URL dates risks breaking pipeline downloads over time. The ingestion module resolves the latest verified link dynamically with user-agent header handling.
- **Verification:** Verified live HTTP/2 200 OK response for NYC compressed gzip file (`listings.csv.gz`, ~15.7 MB compressed, ~38,000+ rows).

---

## 3. Demand Proxy Integrity & Terminology Standard
- **Decision:** Strictly label review-based metrics as **Demand Proxies** across all UI tabs, reports, and code modules.
- **Rationale:** Public Inside Airbnb data consists of listing snapshots and review counts. It does NOT contain private financial transaction receipts or exact booking logs. Claiming review counts represent "actual bookings" is misleading.
- **Formulation:** $Estimated\_Bookings = \frac{reviews\_per\_month}{0.50}$ (San Francisco Model assumption).
- **UI Requirement:** The dashboard displays explicit badges distinguishing **OBSERVED DATA** (raw price, room type, location) from **DERIVED ESTIMATES / PROXIES** (occupancy rate, estimated bookings).

---

## 4. Outlier Strategy: Invalid Records vs. Statistical Outliers
- **Decision:** Distinguish between invalid data entries (removed) and valid statistical market extremes (retained and flagged).
- **Rationale:** Automatically dropping all IQR outliers removes luxury penthouses, high-end suites, and ultra-active listings, distorting market modeling for premium property segments.
- **Segmentation:**
  - **Invalid Records (Removed):** `price <= 0.0`, `accommodates < 1`, invalid coordinates.
  - **Statistical Outliers (Retained & Flagged):** Prices above $Q3 + 1.5 \times IQR$ are preserved in training data; binary flag `is_high_price_outlier` is added for segment analysis.

---

## 5. Target Variable Transformation & Evaluation Metrics
- **Decision:** Model $y = \text{log1p}(price) = \ln(1 + price)$ during training; transform test set predictions back using $\hat{price} = \text{expm1}(\hat{y}) = \exp(\hat{y}) - 1$.
- **Rationale:** Standard `log(price)` fails if price equals zero. `log1p` provides numerical stability near zero and normalizes right-skewed pricing distributions. `expm1` provides exact inverse recovery.
- **Metrics Standard:** Primary evaluation is conducted on original USD currency scale using MAE, RMSE, and $R^2$. Log-scale metrics ($RMSE_{log}$) are recorded secondarily to explain model loss optimization behavior.

---

## 6. Machine Learning Data Leakage Prevention Protocol
- **Decision:** Fit all preprocessing transformers (`StringIndexer`, `OneHotEncoder`, median imputers) **strictly on the 80% train split** inside a unified `pyspark.ml.Pipeline`.
- **Rationale:** Fitting indexers, imputers, or scalers on the full dataset leaks test set statistics into training, producing artificially inflated evaluation metrics.
- **Enforcement:** The test set is transformed passively using `PipelineModel.transform()`. Target-derived features are strictly excluded from input feature vectors.

---

## 7. Model Baselines & Evidence-Based Selection
- **Decision:** Benchmark 4 model configurations: Simple Mean Baseline, Linear Regression, Random Forest Regressor, and Gradient-Boosted Trees (GBT).
- **Rationale:** Evaluating a simple baseline ($R^2 = 0.0$) ensures complex ML models prove incremental predictive value. GBT provides strong non-linear feature interaction modeling.
- **Selection Rule:** Final model selection is strictly evidence-based driven by test set RMSE, MAE, and $R^2$.

---

## 8. Dashboard Real-Time Inference Architecture
- **Decision:** Load pre-trained PySpark `PipelineModel` artifacts in Streamlit using a cached `SparkSession` singleton pattern (`@st.cache_resource`).
- **Rationale:** Continuously re-initializing SparkSession across Streamlit UI re-renders causes thread leaks and slow response times. Caching the singleton session allows fast 1-row DataFrame transformation and real-time prediction rendering (< 500 ms).

---

## 9. Spark Resource Allocation for Student Hardware
- **Decision:** Configure local Spark master to `local[8]`, 4 GB driver memory, 4 GB executor memory, and 8 shuffle partitions (`spark.sql.shuffle.partitions = 8`).
- **Rationale:** Optimized for the target student hardware (AMD Ryzen 9 5900HS 16 threads, 15 GB RAM). Setting shuffle partitions to 8 avoids the default 200 partition shuffle bottleneck on local multi-threaded runs.
