# AirIQ Datasets (224,098 Total Records)

This directory contains all ingested raw and processed datasets used in the AirIQ PySpark MLlib training pipeline, Apache Cassandra database, and analytics platform.

---

## 1. Official Inside Airbnb Datasets (International Hubs)
Official quarterly releases scraped directly from Inside Airbnb (`insideairbnb.com/get-the-data/`):
- **`london_listings.csv`** (215 MB) — London, UK: 59,690 listings in GBP (£).
- **`paris_listings.csv`** (173 MB) — Paris, France: 43,286 listings in EUR (€).
- **`rome_listings.csv`** (101 MB) — Rome, Italy: 33,846 listings in EUR (€).
- **`tokyo_listings.csv`** (116 MB) — Tokyo, Japan: 33,535 listings in JPY (¥).
- **`new_york_listings.csv`** (75 MB) — New York City, USA: 19,299 listings in USD ($).
- **`sydney_listings.csv`** (58 MB) — Sydney, Australia: 17,611 listings in AUD (A$).
- **`amsterdam_listings.csv`** (26 MB) — Amsterdam, Netherlands: 6,032 listings in EUR (€).

---

## 2. Real Indian Metros Datasets (INR - ₹)
Since official Inside Airbnb covers 0 cities in India, authentic scraped datasets were sourced from verified repositories:
- **`real_india_listings.csv`** (1.8 MB) — 10,834 real listings in INR (₹):
  - **Bengaluru:** 7,146 listings (Avg: ₹2,783.78)
  - **Mumbai:** 3,653 listings (Avg: ₹5,706.79)
- **`bangalore_mumbai.csv`** — Source scrape from DoorstepAnalytics covering Bangalore & Mumbai.
- **`india_gems.csv`** — Scraped properties across Goa, Kerala, and Rajasthan.

---

## 3. Directory Layout
```text
dataset/ (alias to data/)
├── raw/
│   ├── real_india_listings.csv
│   ├── london_listings.csv
│   ├── paris_listings.csv
│   ├── rome_listings.csv
│   ├── tokyo_listings.csv
│   ├── new_york_listings.csv
│   ├── sydney_listings.csv
│   ├── amsterdam_listings.csv
│   └── bangalore_mumbai.csv
├── processed/
└── README.md
```
