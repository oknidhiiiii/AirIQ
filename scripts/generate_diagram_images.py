import asyncio
from playwright.async_api import async_playwright
import os

OUT_ARCH_DESKTOP = "/home/adityap/Desktop/system_architecture.png"
OUT_PIPE_DESKTOP = "/home/adityap/Desktop/data_pipeline.png"
LOCAL_ARCH = "presentation/charts/system_architecture.png"
LOCAL_PIPE = "presentation/charts/data_pipeline.png"

ARCH_HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'DejaVu Sans', 'Inter', -apple-system, sans-serif; }
  body {
    width: 1920px;
    height: 1080px;
    background: #0B1120;
    color: #F8FAFC;
    padding: 48px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
  .header {
    border-bottom: 2px solid #1E293B;
    padding-bottom: 20px;
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
  }
  .title {
    font-size: 38px;
    font-weight: 800;
    color: #F8FAFC;
    letter-spacing: -0.5px;
  }
  .title span { color: #FF5A5F; }
  .subtitle {
    font-size: 16px;
    color: #94A3B8;
    margin-top: 6px;
  }
  .badge-row {
    display: flex;
    gap: 12px;
  }
  .badge {
    background: #1E293B;
    border: 1px solid #334155;
    padding: 8px 16px;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 700;
  }
  .badge.coral { color: #FF5A5F; border-color: #E11D48; background: #2A1215; }
  .badge.orange { color: #FB923C; border-color: #EA580C; background: #2A180E; }
  .badge.blue { color: #38BDF8; border-color: #0284C7; background: #082F49; }

  /* Main Grid */
  .grid-container {
    display: grid;
    grid-template-columns: 360px 480px 480px 380px;
    gap: 24px;
    height: 860px;
  }
  .tier-col {
    display: flex;
    flex-direction: column;
    gap: 20px;
  }
  .card {
    background: #131D31;
    border: 1.5px solid #23334E;
    border-radius: 14px;
    padding: 24px;
    display: flex;
    flex-direction: column;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.4);
    position: relative;
  }
  .card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 16px;
    border-bottom: 1px solid #1E293B;
    padding-bottom: 12px;
  }
  .card-title {
    font-size: 18px;
    font-weight: 800;
    color: #F8FAFC;
    display: flex;
    align-items: center;
    gap: 10px;
  }
  .tag {
    font-size: 11px;
    font-weight: 800;
    padding: 4px 8px;
    border-radius: 5px;
    text-transform: uppercase;
  }
  .tag.blue { background: #0369A1; color: #E0F2FE; }
  .tag.coral { background: #BE123C; color: #FFE4E6; }
  .tag.orange { background: #C2410C; color: #FFEDD5; }
  .tag.emerald { background: #047857; color: #D1FAE5; }

  .card-content {
    font-size: 13.5px;
    line-height: 1.6;
    color: #CBD5E1;
  }
  .card-content ul {
    list-style: none;
    padding: 0;
  }
  .card-content li {
    position: relative;
    padding-left: 18px;
    margin-bottom: 10px;
  }
  .card-content li::before {
    content: "▸";
    position: absolute;
    left: 0;
    color: #38BDF8;
    font-weight: bold;
  }
  .highlight {
    color: #F8FAFC;
    font-weight: 700;
  }
  .stat-pill {
    background: #0B1120;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 10px 14px;
    margin-top: 14px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .stat-val {
    font-size: 16px;
    font-weight: 800;
    color: #38BDF8;
  }
</style>
</head>
<body>

<div class="header">
  <div>
    <div class="title">AirIQ: <span>Distributed System Architecture</span></div>
    <div class="subtitle">Multi-City Big Data Rental Intelligence Pipeline • Apache Spark 4.2 MLlib + Apache Cassandra 4.1 + React 19</div>
  </div>
  <div class="badge-row">
    <div class="badge coral">224,098 Total Records</div>
    <div class="badge orange">Apache Spark MLlib</div>
    <div class="badge blue">Cassandra NoSQL</div>
  </div>
</div>

<div class="grid-container">

  <!-- Col 1: Ingestion Sources -->
  <div class="tier-col">
    <div class="card" style="flex: 1; border-color: #38BDF8;">
      <div class="card-header">
        <div class="card-title">1. DATA SOURCES</div>
        <div class="tag blue">RAW INGESTION</div>
      </div>
      <div class="card-content">
        <p style="margin-bottom: 12px; font-weight: bold; color: #38BDF8;">Dual-Dataset Architecture:</p>
        <ul>
          <li><span class="highlight">Official Inside Airbnb (213,264 listings):</span> Quarterly releases covering 7 global hubs (London, Paris, Rome, Tokyo, NYC, Sydney, Amsterdam).</li>
          <li><span class="highlight">DoorstepAnalytics India (10,834 listings):</span> Real scraped listings in INR (₹) covering Mumbai (3,653) & Bengaluru (7,146).</li>
          <li><span class="highlight">Solves Coverage Void:</span> Overcomes Inside Airbnb's total lack of Indian market records.</li>
        </ul>
        <div class="stat-pill">
          <span>Global Hubs Volume</span>
          <span class="stat-val">213,264</span>
        </div>
        <div class="stat-pill">
          <span>Indian Metros Volume</span>
          <span class="stat-val" style="color: #FF5A5F;">10,834</span>
        </div>
      </div>
    </div>
  </div>

  <!-- Col 2: Spark MLlib Engine -->
  <div class="tier-col">
    <div class="card" style="flex: 1; border-color: #FB923C;">
      <div class="card-header">
        <div class="card-title">2. SPARK MLlib ENGINE</div>
        <div class="tag orange">COMPUTE (4.2.0)</div>
      </div>
      <div class="card-content">
        <p style="margin-bottom: 12px; font-weight: bold; color: #FB923C;">In-Memory Distributed ML:</p>
        <ul>
          <li><span class="highlight">PySpark Cleaning & Casting:</span> Regex price cleaning, null rating median imputation (4.5 / 5.0).</li>
          <li><span class="highlight">Currency Normalization:</span> Standardized baseline (`price_usd = price_local * usd_rate`) ensures mathematical stability.</li>
          <li><span class="highlight">StringIndexer:</span> Encodes categorical markets & room types into indexed integers.</li>
          <li><span class="highlight">VectorAssembler:</span> Combines 6 features [city, room, capacity, beds, baths, rating].</li>
          <li><span class="highlight">RandomForestRegressor:</span> Trains 45 parallel decision trees (depth 9) on 80% train split.</li>
        </ul>
        <div class="stat-pill">
          <span>Test Split RMSE</span>
          <span class="stat-val" style="color: #34D399;">$209.98 USD</span>
        </div>
        <div class="stat-pill">
          <span>Error Reduction vs OLS</span>
          <span class="stat-val" style="color: #34D399;">▼ 35.1%</span>
        </div>
      </div>
    </div>
  </div>

  <!-- Col 3: Storage & Microservice -->
  <div class="tier-col">
    <div class="card" style="flex: 1; border-color: #34D399;">
      <div class="card-header">
        <div class="card-title">3. CASSANDRA & API</div>
        <div class="tag emerald">STORAGE & SERVING</div>
      </div>
      <div class="card-content">
        <p style="margin-bottom: 12px; font-weight: bold; color: #34D399;">Distributed Storage & API:</p>
        <ul>
          <li><span class="highlight">Apache Cassandra 4.1.0 (Port 9042):</span> Masterless wide-column ring for high-availability spatial writes.</li>
          <li><span class="highlight">Keyspace Partitioning:</span> Table `city_summary_metrics` partitioned by country; table `listings_by_city` partitioned by (country, city).</li>
          <li><span class="highlight">FastAPI Microservice (Port 8001):</span> Asynchronous non-blocking Python ASGI server.</li>
          <li><span class="highlight">In-Memory Tree Traversal:</span> Pre-loads 45 Spark Parquet trees for live inference in &lt; 15ms.</li>
          <li><span class="highlight">Currency De-normalization:</span> Dynamically maps base USD prediction back into native local currency (₹, ¥, £, €).</li>
        </ul>
        <div class="stat-pill">
          <span>Prediction Latency</span>
          <span class="stat-val" style="color: #34D399;">&lt; 15 ms</span>
        </div>
        <div class="stat-pill">
          <span>Cassandra Query Speed</span>
          <span class="stat-val">&lt; 3 ms</span>
        </div>
      </div>
    </div>
  </div>

  <!-- Col 4: Geospatial Frontend -->
  <div class="tier-col">
    <div class="card" style="flex: 1; border-color: #FF5A5F;">
      <div class="card-header">
        <div class="card-title">4. CLIENT UI</div>
        <div class="tag coral">REACT 19 + VITE</div>
      </div>
      <div class="card-content">
        <p style="margin-bottom: 12px; font-weight: bold; color: #FF5A5F;">Geospatial & Analytics UI:</p>
        <ul>
          <li><span class="highlight">React 19 SPA (Port 5173):</span> Responsive component architecture built with Tailwind CSS.</li>
          <li><span class="highlight">Leaflet Marker Clustering:</span> Dynamically aggregates dense pins into clickable badges; eliminates DOM lag.</li>
          <li><span class="highlight">Zero Blurry Heatmaps:</span> Transparent pin inspection showing exact neighborhood, price, and rating.</li>
          <li><span class="highlight">Verified Land Coordinates:</span> 14,000 spatial pins checked within legitimate land boundaries.</li>
          <li><span class="highlight">Native Currency UI:</span> Displays ₹ INR, ¥ JPY, £ GBP, € EUR, A$ AUD, and $ USD.</li>
        </ul>
        <div class="stat-pill">
          <span>Markets Supported</span>
          <span class="stat-val" style="color: #FF5A5F;">9 Cities</span>
        </div>
        <div class="stat-pill">
          <span>DOM Performance</span>
          <span class="stat-val">Zero Lag (Clustered)</span>
        </div>
      </div>
    </div>
  </div>

</div>

</body>
</html>
"""

PIPE_HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'DejaVu Sans', 'Inter', -apple-system, sans-serif; }
  body {
    width: 1920px;
    height: 1080px;
    background: #0B1120;
    color: #F8FAFC;
    padding: 48px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
  .header {
    border-bottom: 2px solid #1E293B;
    padding-bottom: 20px;
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
  }
  .title {
    font-size: 38px;
    font-weight: 800;
    color: #F8FAFC;
    letter-spacing: -0.5px;
  }
  .title span { color: #38BDF8; }
  .subtitle {
    font-size: 16px;
    color: #94A3B8;
    margin-top: 6px;
  }
  
  /* Pipeline 5-Column Flow */
  .pipe-flow {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 20px;
    height: 860px;
    position: relative;
  }
  .pipe-card {
    background: #131D31;
    border: 2px solid #1E293B;
    border-radius: 14px;
    padding: 24px;
    display: flex;
    flex-direction: column;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.4);
    position: relative;
  }
  .step-num {
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 1px;
    color: #38BDF8;
    margin-bottom: 6px;
    text-transform: uppercase;
  }
  .step-title {
    font-size: 20px;
    font-weight: 800;
    color: #F8FAFC;
    margin-bottom: 16px;
    padding-bottom: 12px;
    border-bottom: 1px solid #1E293B;
  }
  .step-content {
    font-size: 13.5px;
    line-height: 1.6;
    color: #CBD5E1;
    flex: 1;
  }
  .step-content ul {
    list-style: none;
    padding: 0;
  }
  .step-content li {
    position: relative;
    padding-left: 18px;
    margin-bottom: 12px;
  }
  .step-content li::before {
    content: "▸";
    position: absolute;
    left: 0;
    color: #38BDF8;
    font-weight: bold;
  }
  .highlight {
    color: #F8FAFC;
    font-weight: 700;
  }
  .tag-box {
    background: #0B1120;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 12px;
    margin-top: 14px;
    font-size: 13px;
    color: #94A3B8;
  }
  .tag-box strong { color: #38BDF8; display: block; margin-bottom: 4px; }
  
  .c1 { border-top: 6px solid #38BDF8; }
  .c2 { border-top: 6px solid #FB923C; }
  .c3 { border-top: 6px solid #A855F7; }
  .c4 { border-top: 6px solid #34D399; }
  .c5 { border-top: 6px solid #FF5A5F; }
</style>
</head>
<body>

<div class="header">
  <div>
    <div class="title">AirIQ: <span>End-to-End Data & ML Pipeline</span></div>
    <div class="subtitle">5-Stage Distributed Processing Pipeline from Ingestion to Real-Time Geospatial Serving</div>
  </div>
  <div style="font-size: 15px; color: #94A3B8; font-weight: bold;">
    Total Volume: <span style="color: #FF5A5F;">224,098 Records</span> | 9 Global Markets
  </div>
</div>

<div class="pipe-flow">

  <!-- Step 1 -->
  <div class="pipe-card c1">
    <div class="step-num">STAGE 01</div>
    <div class="step-title">Ingestion</div>
    <div class="step-content">
      <ul>
        <li><span class="highlight">213,264 Global Listings:</span> Official quarterly releases from Inside Airbnb (London, Paris, Rome, Tokyo, NYC, Sydney, Amsterdam).</li>
        <li><span class="highlight">10,834 Real Indian Listings:</span> DoorstepAnalytics scrape covering Bengaluru & Mumbai.</li>
        <li><span class="highlight">Multi-Format Extraction:</span> Multi-line CSV ingestion with quote and comma escape handling.</li>
      </ul>
      <div class="tag-box">
        <strong>OUTPUT:</strong>
        Unified raw Spark DataFrame with 224,098 listings across 9 destinations.
      </div>
    </div>
  </div>

  <!-- Step 2 -->
  <div class="pipe-card c2">
    <div class="step-num">STAGE 02</div>
    <div class="step-title">PySpark ETL</div>
    <div class="step-content">
      <ul>
        <li><span class="highlight">Symbol Stripping:</span> Regex cleaning of currency signs ($, £, €, ¥, ,).</li>
        <li><span class="highlight">Data Type Casting:</span> Explicit double precision on latitude, longitude, price, accommodates.</li>
        <li><span class="highlight">Null Value Imputation:</span> Fills missing host review scores with cluster median (4.5 / 5.0).</li>
        <li><span class="highlight">USD Normalization:</span> Standardized baseline (`price_usd = price_local * usd_rate`).</li>
      </ul>
      <div class="tag-box">
        <strong>OUTPUT:</strong>
        Cleaned, type-casted DataFrame retaining both `price_local` and `price_usd`.
      </div>
    </div>
  </div>

  <!-- Step 3 -->
  <div class="pipe-card c3">
    <div class="step-num">STAGE 03</div>
    <div class="step-title">MLlib Training</div>
    <div class="step-content">
      <ul>
        <li><span class="highlight">StringIndexer:</span> Encodes categorical markets & room privacy types into index columns.</li>
        <li><span class="highlight">VectorAssembler:</span> Merges 6 core features: [city, room, capacity, beds, baths, rating].</li>
        <li><span class="highlight">80/20 Random Split:</span> 179,826 train rows / 44,272 evaluation test rows.</li>
        <li><span class="highlight">RandomForestRegressor:</span> 45 parallel trees, max depth 9, variance reduction criterion.</li>
      </ul>
      <div class="tag-box">
        <strong>MODEL ACCURACY:</strong>
        RMSE = $209.98 USD, MAE = $114.58 USD, R² = 0.3659 (35.1% error reduction).
      </div>
    </div>
  </div>

  <!-- Step 4 -->
  <div class="pipe-card c4">
    <div class="step-num">STAGE 04</div>
    <div class="step-title">Cassandra Sink</div>
    <div class="step-content">
      <ul>
        <li><span class="highlight">Wide-Column Modeling:</span> CQL schema on port 9042 with replication strategy.</li>
        <li><span class="highlight">City Metrics Table:</span> `city_summary_metrics` partitioned by `country`, clustered by `city`.</li>
        <li><span class="highlight">Spatial Listings Table:</span> `listings_by_city` partitioned by `(country, city)` for immediate bounding queries.</li>
        <li><span class="highlight">Sub-Millisecond Read:</span> Pre-aggregated stats deliver instant dashboard cards.</li>
      </ul>
      <div class="tag-box">
        <strong>DATABASE SINK:</strong>
        9 city summary aggregates + 14,000 spatial listing pins loaded in Cassandra.
      </div>
    </div>
  </div>

  <!-- Step 5 -->
  <div class="pipe-card c5">
    <div class="step-num">STAGE 05</div>
    <div class="step-title">Real-Time Serving</div>
    <div class="step-content">
      <ul>
        <li><span class="highlight">FastAPI Microservice (Port 8001):</span> Loads 45 Spark Parquet trees directly into native memory on boot.</li>
        <li><span class="highlight">Sub-15ms Inference:</span> Traverses decision trees without PySpark JVM lag.</li>
        <li><span class="highlight">Currency De-normalization:</span> Base USD predictions dynamically converted into local currency (₹, ¥, £, €).</li>
        <li><span class="highlight">Leaflet Marker Clustering:</span> React 19 UI clusters pins to ensure zero DOM lag.</li>
      </ul>
      <div class="tag-box">
        <strong>CLIENT DELIVERABLE:</strong>
        Instant pricing recommendations with upper/lower bounds + interactive maps.
      </div>
    </div>
  </div>

</div>

</body>
</html>
"""

async def generate():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            executable_path="/usr/bin/google-chrome",
            args=["--no-sandbox", "--disable-setuid-sandbox"]
        )
        context = await browser.new_context(viewport={"width": 1920, "height": 1080})
        page = await context.new_page()

        # 1. System Architecture
        await page.set_content(ARCH_HTML)
        await page.wait_for_timeout(1000)
        await page.screenshot(path=OUT_ARCH_DESKTOP)
        await page.screenshot(path=LOCAL_ARCH)
        print(f"[+] Saved System Architecture Diagram to: {OUT_ARCH_DESKTOP}")

        # 2. Data Pipeline
        await page.set_content(PIPE_HTML)
        await page.wait_for_timeout(1000)
        await page.screenshot(path=OUT_PIPE_DESKTOP)
        await page.screenshot(path=LOCAL_PIPE)
        print(f"[+] Saved Data Pipeline Flow Diagram to: {OUT_PIPE_DESKTOP}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(generate())
