# AirIQ Environment Setup & Execution Guide
## AirIQ: Airbnb Pricing & Market Intelligence Using Apache PySpark

---

## 1. Verified Environment Compatibility Matrix

The AirIQ execution environment has been empirically verified via Spark smoke testing:

| Component | Verified Specification | Compatibility Notes |
| :--- | :--- | :--- |
| **Python** | `Python 3.14.7` | Verified compatible with PySpark 3.5.1 |
| **Java JVM** | `OpenJDK 21.0.12.1` | Verified OpenJDK 21 LTS runtime |
| **Apache PySpark** | `PySpark 3.5.1` | Verified local cluster master (`local[8]`) |
| **Operating System**| Linux (Debian-based) | Tested on AMD Ryzen 9 5900HS (16 threads, 15 GB RAM) |

---

## 2. Step-by-Step Installation Instructions

### Step 1: Change to Workspace Directory
```bash
cd /home/adityap/ai/Projects/AirIQ
```

### Step 2: Verify System Java Version
```bash
java -version
```
*Expected Output:* `openjdk version "21.0.12.1"` or OpenJDK 17+.

### Step 3: Create & Activate Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 4: Install Dependencies & Package
```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
pip install -e .
```

---

## 3. End-to-End Phase 1 Pipeline Execution Commands

### Mandatory Step 0: Run PySpark Smoke Test
```bash
airiq smoke-test
```
*Expected Output:* `SPARK SMOKE TEST STATUS: PASSED!`

### Master Step 1: Execute Complete Phase 1 Pipeline
```bash
airiq run-phase1
```
*Outputs Created:*
- `data/raw/listings.csv.gz` (Raw gzip compressed dataset, ~15.7 MB)
- `data/raw/listings_metadata.json` (Provenance tracking file)
- `data/outputs/raw_data_profile.json` (Structured data quality and profiling report)

### Individual Phase 1 Commands
```bash
# Download dataset only
airiq download-data

# Validate raw data non-destructively
airiq validate-raw

# Profile raw dataset
airiq profile-raw

# Execute PyTest unit test suite
pytest tests/ -v
```
