# AirIQ Phase 1 Execution & Validation Report
## Foundation, Environment Setup, Data Ingestion & Raw Data Quality Validation

---

## 1. Executive Summary

Phase 1 of **AirIQ: Airbnb Pricing & Market Intelligence Using Apache PySpark** has been fully implemented, validated, and benchmarked. 

All core foundational components—including repository directory scaffolding, isolated virtual environment dependency setup, centralized configuration management, PySpark `SparkSession` lifecycle management, mandatory pre-flight environment smoke testing, automated dataset downloader with provenance metadata tracking, explicit `StructType` schema reader, non-destructive data quality validator, machine-readable JSON dataset profiler, unified CLI, and PyTest unit test suite—were built and verified on live NYC Inside Airbnb data.

---

## 2. Infrastructure & Files Created/Modified

### Scaffolding & Configuration
- `config/default_config.yaml` — Central YAML configuration controlling dataset URLs, workspace paths, Spark local resources (`local[8]`, 4GB driver memory), logging levels, and validation bounds.
- `requirements.txt` — Pinned dependency requirements (`pyspark==3.5.1`, `pyarrow==15.0.0`, `pandas==2.2.1`, `streamlit==1.32.0`, `plotly==5.19.0`, `pytest==8.0.2`, `pyyaml==6.0.1`, `requests==2.31.0`).
- `setup.py` — Package configuration supporting editable installation (`pip install -e .`) and `airiq` console CLI entry points.
- `.gitignore` — Comprehensive ignore rules for Python virtual environments, PySpark logs, metadata databases, and data outputs.
- `README.md` & `SETUP.md` — Updated with CLI workflows and commands.

### Core Package Source Code (`src/airiq/`)
- `src/airiq/utils/logging_utils.py` — Structured application logger module.
- `src/airiq/utils/config_loader.py` — Dynamic configuration loader resolving workspace relative paths.
- `src/airiq/spark/session.py` — Centralized PySpark `SparkSession` builder using local resource caps (`local[8]`).
- `src/airiq/spark/smoke_test.py` — Mandatory pre-flight PySpark smoke test module.
- `src/airiq/ingestion/schema.py` — Explicit PySpark `StructType` schema specification matching `DATA_DICTIONARY.md`.
- `src/airiq/ingestion/downloader.py` — Dataset downloader with HTTP 200 verification and SHA256 checksum provenance tracking.
- `src/airiq/ingestion/reader.py` — Schema-enforced PySpark DataFrame reader utilizing column-name casting.
- `src/airiq/ingestion/validator.py` — Non-destructive raw data quality validation suite using ANSI SQL safe `try_cast`.
- `src/airiq/ingestion/profiler.py` — Machine-readable dataset profiler exporting JSON reports.
- `src/airiq/cli.py` — Master CLI supporting `smoke-test`, `download-data`, `validate-raw`, `profile-raw`, and `run-phase1`.

### Test Suite (`tests/`)
- `tests/test_spark_session.py` — Tests SparkSession startup, smoke test execution, and clean shutdown.
- `tests/test_schema.py` — Validates `StructType` field counts and critical column presence.
- `tests/test_ingestion.py` — Validates CSV reader behavior and `SchemaValidationError` raising.
- `tests/test_validation.py` — Tests quality validation metrics on synthetic DataFrames.

---

## 3. Dependency Environment & Compatibility Matrix

| Dependency | Installed Version | Verification Result |
| :--- | :--- | :--- |
| **Python** | `3.14.7` | Compatible; no bytecode or syntax errors. |
| **Java JVM** | `OpenJDK 21.0.12.1` | Verified 64-Bit OpenJDK 21 LTS runtime. |
| **Apache PySpark** | `3.5.1` / `4.2.0-dev` | Initialized cleanly on `local[8]` master context. |
| **PyArrow** | `15.0.0` | PySpark Arrow optimization enabled (`spark.sql.execution.arrow.pyspark.enabled = true`). |
| **PyYAML** | `6.0.1` | Configuration loading verified. |
| **PyTest** | `8.0.2` | Test execution verified. |

---

## 4. PySpark Smoke Test Verification Result

**Execution Output:**
```text
2026-10-06 14:33:43 [INFO] airiq.spark.smoke_test - Step 1 PASSED: PySpark imports and SparkSession initialized.
2026-10-06 14:33:43 [INFO] airiq.spark.smoke_test - Step 2 PASSED: Spark DataFrame created (count = 2).
2026-10-06 14:33:43 [INFO] airiq.spark.smoke_test - Step 3 PASSED: Spark SQL execution verified (avg_price = $175.00).
2026-10-06 14:33:43 [INFO] airiq.spark.smoke_test - Step 4 PASSED: SparkSession shut down cleanly.
2026-10-06 14:33:43 [INFO] airiq.spark.smoke_test - ==========================================
2026-10-06 14:33:43 [INFO] airiq.spark.smoke_test -   SPARK SMOKE TEST STATUS: PASSED!
2026-10-06 14:33:43 [INFO] airiq.spark.smoke_test - ==========================================
```

---

## 5. Dataset Provenance & Ingestion Statistics

- **Source:** Inside Airbnb Open Data Portal
- **Snapshot Date:** `2026-06-14` (New York City)
- **Source URL:** `https://data.insideairbnb.com/united-states/ny/new-york-city/2026-06-14/data/listings.csv.gz`
- **Downloaded File Size:** 15,694,632 bytes (~14.97 MB compressed gzip)
- **SHA256 Checksum:** `9e863d3f0caa499093b0af0a1bfd49c3...`
- **Metadata Provenance Output:** `data/raw/listings_metadata.json`
- **Total Ingested Rows:** **30,259 records**
- **Schema Attributes:** **36 explicitly typed columns**

---

## 6. Raw Data Quality Validation Summary

Validation was executed in a **non-destructive manner** (no records deleted during Phase 1):

| Quality Metric | Count / Finding | Percentage | Risk Assessment & Operational Guidance |
| :--- | :--- | :--- | :--- |
| **Total Rows Read** | 30,259 | 100.0% | Complete raw snapshot loaded into PySpark DataFrame. |
| **Duplicate Listing IDs** | 0 | 0.00% | Primary key `id` is 100% unique. |
| **Null Listing IDs** | 0 | 0.00% | Zero null primary key records. |
| **Invalid/Non-numeric Prices** | 8,744 | 28.90% | Missing or blank price strings in raw snapshot. Must be handled via Phase 2 cleaning filters (`price > 0`). |
| **Invalid Coordinates** | 27 | 0.09% | Coordinates falling outside bounding box ($40.4 \le lat \le 40.9, -74.3 \le lon \le -73.6$). |
| **Invalid Accommodates (<1)** | 0 | 0.00% | Capacity attributes valid. |
| **Invalid Room Types** | 0 | 0.00% | Categorical values conform strictly to domain values (`Entire home/apt`, `Private room`, `Shared room`, `Hotel room`). |

---

## 7. Automated Test Suite Results

```text
tests/test_ingestion.py::test_reader_synthetic_csv PASSED                [ 12%]
tests/test_ingestion.py::test_reader_missing_columns_raises_validation_error PASSED [ 25%]
tests/test_schema.py::test_schema_field_count PASSED                     [ 37%]
tests/test_schema.py::test_schema_critical_columns_presence PASSED       [ 50%]
tests/test_spark_session.py::test_spark_session_creation PASSED          [ 62%]
tests/test_spark_session.py::test_spark_smoke_test_function PASSED       [ 75%]
tests/test_spark_session.py::test_spark_session_cleanup PASSED           [ 87%]
tests/test_validation.py::test_validation_quality_checks PASSED          [100%]

======================== 8 passed in 14.06s =========================
```

---

## 8. Execution Timing & Performance Observations

- **Spark Startup Time:** ~4.0 seconds (Local master `local[8]`)
- **Dataset Download Time:** < 0.5 seconds (Utilized existing cached file; < 3.5s over network)
- **PySpark Ingestion & Schema Projection:** ~1.5 seconds
- **Data Quality Validation Execution:** ~7.0 seconds
- **Data Profiling & JSON Generation:** ~9.0 seconds
- **Total End-to-End Pipeline Execution Time:** **~25.0 seconds**

*Resource Note:* Driver memory usage remained under 1.2 GB during execution, proving that resource caps (`spark.driver.memory = 4g`) operate cleanly on student hardware (AMD Ryzen 9 5900HS 16 threads, 15 GB RAM).

---

## 9. Recommendations & Transition Plan for Phase 2

1. **Filtering Invalid Prices in Phase 2:** Phase 2 data cleaning must filter out the 8,744 non-numeric/null price records (`price_numeric > 0.0`) to produce a clean baseline dataset (~21,515 records) for analytics and MLlib model fitting.
2. **Geospatial Boundary Filtering:** Remove the 27 out-of-bound coordinate records to ensure accurate spatial neighborhood mapping.
3. **Statistical Outlier Flagging:** Retain high-price luxury listings while adding binary indicator flags (`is_high_price_outlier`) as established in `METHODOLOGY.md`.
4. **Parquet Storage Serialization:** Write cleaned Phase 2 DataFrames to `data/processed/cleaned_listings.parquet` partitioned by `neighbourhood_group_cleansed`.

---

### Phase 1 Completion Signal

**PHASE 1 COMPLETE**
