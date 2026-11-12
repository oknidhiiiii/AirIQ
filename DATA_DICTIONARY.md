# AirIQ Data Dictionary & Schema Specification
## AirIQ: Airbnb Pricing & Market Intelligence Using Apache PySpark

---

## 1. Raw Input Schema (`listings.csv` / `listings.csv.gz`)

The raw schema is explicitly defined in `airiq/ingestion/schema.py` using PySpark `StructType` to prevent costly schema inference scans.

| Column Name | Raw Spark Type | Nullable | Description & Domain Values |
| :--- | :--- | :--- | :--- |
| `id` | `LongType` | False | Unique listing identifier |
| `name` | `StringType` | True | Title / description of the listing |
| `host_id` | `LongType` | False | Unique host identifier |
| `host_name` | `StringType` | True | Name of the listing host |
| `host_since` | `DateType` | True | Date host joined Airbnb (`YYYY-MM-DD`) |
| `host_location` | `StringType` | True | Host location string |
| `host_is_superhost` | `StringType` | True | Superhost flag (`t` / `f`) |
| `host_listings_count` | `IntegerType` | True | Total listings count owned by host |
| `neighbourhood` | `StringType` | True | Neighbourhood description |
| `neighbourhood_cleansed` | `StringType` | True | Standardized neighbourhood name |
| `neighbourhood_group_cleansed` | `StringType` | True | Borough / Region group (e.g., Manhattan, Brooklyn) |
| `latitude` | `DoubleType` | True | Latitude coordinate |
| `longitude` | `DoubleType` | True | Longitude coordinate |
| `property_type` | `StringType` | True | Specific property classification |
| `room_type` | `StringType` | True | Category (`Entire home/apt`, `Private room`, `Shared room`, `Hotel room`) |
| `accommodates` | `IntegerType` | True | Maximum guest capacity |
| `bathrooms` | `DoubleType` | True | Number of bathrooms |
| `bedrooms` | `IntegerType` | True | Number of bedrooms |
| `beds` | `IntegerType` | True | Number of beds |
| `price` | `StringType` | False | Listing nightly price string (e.g., `"$150.00"`) |
| `minimum_nights` | `IntegerType` | True | Minimum stay requirement in nights |
| `maximum_nights` | `IntegerType` | True | Maximum stay limit in nights |
| `availability_30` | `IntegerType` | True | Days available in next 30 days |
| `availability_60` | `IntegerType` | True | Days available in next 60 days |
| `availability_90` | `IntegerType` | True | Days available in next 90 days |
| `availability_365` | `IntegerType` | True | Days available in next 365 days |
| `number_of_reviews` | `IntegerType` | True | Total cumulative guest reviews |
| `number_of_reviews_ltm` | `IntegerType` | True | Total reviews received in last 12 months |
| `reviews_per_month` | `DoubleType` | True | Average monthly review volume |
| `review_scores_rating` | `DoubleType` | True | Overall review rating score |
| `review_scores_cleanliness` | `DoubleType` | True | Cleanliness sub-score |
| `review_scores_checkin` | `DoubleType` | True | Check-in sub-score |
| `review_scores_communication`| `DoubleType` | True | Communication sub-score |
| `review_scores_location` | `DoubleType` | True | Location sub-score |
| `review_scores_value` | `DoubleType` | True | Value sub-score |
| `calculated_host_listings_count` | `IntegerType` | True | Computed active listing count per host |

---

## 2. Transformed & Engineered Dataset Schema (`cleaned_listings.parquet`)

| Column Name | Transformed Type | Category Type | Derived From & Formula |
| :--- | :--- | :--- | :--- |
| `price` | `DoubleType` | OBSERVED | `cast(regexp_replace(price, '[\$,]', '') as Double)` |
| `log_price` | `DoubleType` | DERIVED | $\text{log1p}(price) = \ln(1 + price)$ — Target variable for MLlib regression |
| `is_invalid_record` | `IntegerType` | FILTER FLAG | `when(price <= 0 OR accommodates < 1, 1).otherwise(0)` |
| `is_high_price_outlier` | `IntegerType` | STATISTICAL FLAG | `when(price > Q3 + 1.5*IQR, 1).otherwise(0)` (Retained for analysis) |
| `host_is_superhost_num` | `IntegerType` | OBSERVED | `when(host_is_superhost == 't', 1).otherwise(0)` |
| `host_tenure_years` | `DoubleType` | OBSERVED | `floor((current_date() - host_since) / 365.25)` |
| `estimated_monthly_bookings` | `DoubleType` | DEMAND PROXY | $\frac{reviews\_per\_month}{0.50}$ (San Francisco Model Assumption Proxy) |
| `estimated_occupancy_rate` | `DoubleType` | DEMAND PROXY | $\min\left(\frac{estimated\_monthly\_bookings \times 3}{90}, 1.0\right)$ |
| `estimated_monthly_revenue` | `DoubleType` | DEMAND PROXY | $estimated\_monthly\_bookings \times \max(minimum\_nights, 3) \times price$ |
| `rating_imputed_flag` | `IntegerType` | DATA QUALITY | `when(raw_rating.isNull, 1).otherwise(0)` |

---

## 3. Data Integrity & Labeling Protocol

To enforce transparency:
- **OBSERVED DATA:** Metrics extracted directly from raw dataset without assumption modeling (e.g. `price`, `room_type`, `accommodates`, `number_of_reviews`, `availability_365`).
- **DERIVED DATA / PROXIES:** Metrics calculated via mathematical transformation or research assumptions (e.g. `log_price`, `estimated_monthly_bookings`, `estimated_occupancy_rate`).
