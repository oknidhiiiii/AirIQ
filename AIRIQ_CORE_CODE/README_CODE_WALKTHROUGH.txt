========================================================================================
AIRIQ: CORE RUNNING CODE WALKTHROUGH & LAB VIVA DEFENSE GUIDE
========================================================================================
If your guide (Dr. Preeti G. Khante) or lab examiner asks: "Show me where the project runs,"
open this folder. It is structured into 5 logical modules matching the Big Data syllabus:

----------------------------------------------------------------------------------------
FOLDER 01: SPARK MLlib DISTRIBUTED PIPELINE
File: 01_SPARK_MLLIB_PIPELINE/train_pipeline.py
----------------------------------------------------------------------------------------
What to tell Mam:
"This is our Apache Spark 4.2 data pipeline written in PySpark. It ingests all 224,098 
listings in parallel, cleans foreign currency symbols, imputes null values, and trains 
our Machine Learning model."

Key Code Sections to point at:
• Lines 40-95:   Multi-City Ingestion (Loads Inside Airbnb global datasets + DoorstepAnalytics India CSV).
• Lines 125-148: Multi-Currency Normalization (Derives standardized `price_usd` for statistical consistency).
• Lines 182-195: PySpark StringIndexer (Encodes categorical `city` and `room_type` into numeric indices).
• Lines 202-205: VectorAssembler (Combines 6 features into a single Spark dense feature vector).
• Lines 208-215: RandomForestRegressor (Trains 45 parallel trees with max depth 9 on 80% train split).
• Lines 216-224: RegressionEvaluator (Calculates RMSE $209.98, MAE $114.58, and R² 0.3659 on test split).
• Lines 245-295: Apache Cassandra Sink (Batched partition writes to `city_summary_metrics` and `listings_by_city`).


----------------------------------------------------------------------------------------
FOLDER 02: APACHE CASSANDRA NoSQL DATABASE
File: 02_CASSANDRA_DATABASE/schema.cql
----------------------------------------------------------------------------------------
What to tell Mam:
"This is our CQL (Cassandra Query Language) DDL script defining our NoSQL keyspace and 
partitioning strategy on port 9042."

Key Code Sections to point at:
• `CREATE KEYSPACE airbnb_intelligence`: NetworkTopology / SimpleStrategy with replication factor.
• Table 1 `city_summary_metrics`:
  - Partition Key: `country`, Clustering Key: `city`.
  - Enables instant retrieval of city macro averages (₹2,783 in Bengaluru, ₹5,706 in Mumbai).
• Table 2 `listings_by_city`:
  - Partition Key: `(country, city)`, Clustering Key: `listing_id`.
  - Distributes millions of spatial records across the Cassandra ring for sub-millisecond map loading.


----------------------------------------------------------------------------------------
FOLDER 03: FASTAPI BACKEND SERVER & REAL-TIME ML INFERENCE
File: 03_FASTAPI_BACKEND_SERVER/main.py
----------------------------------------------------------------------------------------
What to tell Mam:
"This is our high-concurrency FastAPI microservice running on port 8001. It loads our 
trained Spark Random Forest trees directly into memory and executes live predictions in < 15ms."

Key Code Sections to point at:
• Lines 60-95:   `load_spark_model_trees()` (Parses Spark Parquet decision trees into memory on startup).
• Lines 98-118:  `evaluate_spark_tree()` (Pure-Python recursive traversal across all 45 decision trees).
• Lines 140-165: `/api/v1/cities` (Queries Cassandra for live multi-city statistical cards).
• Lines 168-195: `/api/v1/listings` (Fetches spatial coordinates for map rendering).
• Lines 255-305: `/api/v1/predict` (Accepts form inputs, runs Spark tree evaluation, and de-normalizes 
                 USD output into native local currency: ₹ INR, ¥ JPY, £ GBP, € EUR).


----------------------------------------------------------------------------------------
FOLDER 04: REACT 19 GEOSPATIAL & ANALYTICS FRONTEND
Files:
1. `PricePrediction.jsx`     (Prediction form, interactive capacity toggles, native currency card)
2. `GeographicExplorer.jsx`  (Leaflet map with `react-leaflet-cluster` for zero DOM lag)
3. `OverviewDashboard.jsx`   (Global & Indian city metrics, live cluster health monitors)
4. `ModelEvaluation.jsx`     (Recharts empirical benchmark against linear regression baseline)
5. `Layout.jsx`              (Global responsive navigation shell & cluster telemetry sidebar)
----------------------------------------------------------------------------------------
What to tell Mam:
"This is our React 19 single-page application. In `GeographicExplorer.jsx`, we implemented 
client-side Marker Clustering so thousands of pins aggregate into interactive badges without 
lagging the browser DOM. In `PricePrediction.jsx`, hosts receive instant fair prices in their 
native currency (₹ INR for India). In `ModelEvaluation.jsx`, we benchmark PySpark's Random Forest 
against heuristic regression."


----------------------------------------------------------------------------------------
FOLDER 05: PRESENTATION GENERATOR SCRIPT
File: 05_PRESENTATION_GENERATOR/generate_pptx.py
----------------------------------------------------------------------------------------
What to tell Mam:
"This is the Python script using `python-pptx` that programmatically builds our 12-slide 
widescreen presentation deck with official logos, screenshots, and evaluation metrics."
========================================================================================
Authors: Aditya Raju Pidurkar (Roll No. 40) & Nidhi Singh (Roll No. 15)
Department of Computer Science & Engineering | RBU
========================================================================================
