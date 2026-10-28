import asyncio
from playwright.async_api import async_playwright
import os

OUT_DESKTOP = "/home/adityap/Desktop/simple_system_flowchart.png"
OUT_DESKTOP_ALT = "/home/adityap/Desktop/system_flow_top_down.png"
LOCAL_OUT = "presentation/charts/simple_system_flowchart.png"
os.makedirs("presentation/charts", exist_ok=True)

HTML_CONTENT = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'DejaVu Sans', 'Inter', -apple-system, sans-serif; }
  body {
    width: 1200px;
    height: 1650px;
    background: #F8FAFC;
    color: #0F172A;
    padding: 40px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  .header {
    text-align: center;
    margin-bottom: 28px;
    width: 100%;
  }
  .title {
    font-size: 36px;
    font-weight: 800;
    color: #0F172A;
    letter-spacing: -0.5px;
  }
  .title span { color: #0284C7; }
  .subtitle {
    font-size: 16px;
    color: #64748B;
    margin-top: 6px;
    font-weight: 500;
  }
  .badges {
    display: flex;
    justify-content: center;
    gap: 12px;
    margin-top: 14px;
  }
  .badge {
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 700;
  }
  .badge.blue { background: #E0F2FE; color: #0369A1; border: 1px solid #BAE6FD; }
  .badge.orange { background: #FFEDD5; color: #C2410C; border: 1px solid #FED7AA; }
  .badge.green { background: #DCFCE7; color: #15803D; border: 1px solid #BBF7D0; }

  /* Flow Container */
  .flow-container {
    width: 960px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0px;
  }

  /* Step Card */
  .step-card {
    width: 100%;
    background: #FFFFFF;
    border: 2px solid #E2E8F0;
    border-radius: 16px;
    padding: 24px 28px;
    box-shadow: 0 4px 16px rgba(15, 23, 42, 0.05);
    display: flex;
    gap: 22px;
    align-items: flex-start;
    position: relative;
  }
  .step-card.blue { border-color: #0284C7; }
  .step-card.orange { border-color: #EA580C; }
  .step-card.purple { border-color: #7C3AED; }
  .step-card.indigo { border-color: #4F46E5; }
  .step-card.emerald { border-color: #059669; }

  /* Step Number Bubble */
  .step-num {
    width: 54px;
    height: 54px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    font-weight: 800;
    color: #FFFFFF;
    flex-shrink: 0;
  }
  .step-card.blue .step-num { background: #0284C7; }
  .step-card.orange .step-num { background: #EA580C; }
  .step-card.purple .step-num { background: #7C3AED; }
  .step-card.indigo .step-num { background: #4F46E5; }
  .step-card.emerald .step-num { background: #059669; }

  .step-body {
    flex: 1;
  }
  .step-title-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
  }
  .step-title {
    font-size: 20px;
    font-weight: 800;
    color: #0F172A;
  }
  .step-tag {
    font-size: 11px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    padding: 4px 10px;
    border-radius: 6px;
  }
  .step-card.blue .step-tag { background: #E0F2FE; color: #0369A1; }
  .step-card.orange .step-tag { background: #FFEDD5; color: #C2410C; }
  .step-card.purple .step-tag { background: #F3E8FF; color: #6D28D9; }
  .step-card.indigo .step-tag { background: #EEF2FF; color: #4338CA; }
  .step-card.emerald .step-tag { background: #DCFCE7; color: #15803D; }

  .step-desc {
    font-size: 14.5px;
    color: #334155;
    line-height: 1.6;
    margin-bottom: 12px;
  }
  .step-desc strong { color: #0F172A; }

  .pills-row {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
  }
  .pill {
    background: #F8FAFC;
    border: 1px solid #CBD5E1;
    border-radius: 8px;
    padding: 5px 12px;
    font-size: 12.5px;
    font-weight: 600;
    color: #475569;
  }
  .pill.highlight {
    background: #F1F5F9;
    color: #0F172A;
    font-weight: 700;
    border-color: #94A3B8;
  }

  /* Connecting Arrow */
  .arrow-connector {
    height: 48px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    position: relative;
  }
  .arrow-line {
    width: 3px;
    height: 32px;
    background: #94A3B8;
  }
  .arrow-head {
    width: 0;
    height: 0;
    border-left: 7px solid transparent;
    border-right: 7px solid transparent;
    border-top: 10px solid #94A3B8;
  }

  .footer-note {
    margin-top: 24px;
    text-align: center;
    font-size: 13px;
    color: #64748B;
    font-weight: 500;
  }
</style>
</head>
<body>

  <div class="header">
    <div class="title">AirIQ: <span>Simple System Flow Flowchart</span></div>
    <div class="subtitle">Top-Down 5-Step Pipeline Architecture &bull; From Raw Data Collection to Low-Latency Serving</div>
    <div class="badges">
      <div class="badge blue">224,098 Total Records</div>
      <div class="badge orange">Apache Spark 4.2 MLlib</div>
      <div class="badge green">Cassandra + FastAPI + React</div>
    </div>
  </div>

  <div class="flow-container">

    <!-- STEP 1: DATA COLLECTION -->
    <div class="step-card blue">
      <div class="step-num">1</div>
      <div class="step-body">
        <div class="step-title-row">
          <div class="step-title">Data Collection & Ingestion</div>
          <span class="step-tag">Dual-Source Provenance</span>
        </div>
        <div class="step-desc">
          Ingests <strong>224,098 total listings</strong> across 12 CSV archives (777 MB) to bridge the global-India coverage gap:
          <br>&bull; <strong>Inside Airbnb:</strong> 213,264 official listings across 7 global hubs (London, Paris, Rome, Tokyo, NYC, Sydney, Amsterdam).
          <br>&bull; <strong>DoorStepAnalytics:</strong> 10,834 real scraped listings in INR (&#8377;) for Mumbai & Bengaluru (solves India void).
        </div>
        <div class="pills-row">
          <div class="pill highlight">224,098 Listings</div>
          <div class="pill">9 Destinations</div>
          <div class="pill">6 Sovereign Currencies (&#8377;, &#165;, &#163;, &#8364;, A$, $)</div>
          <div class="pill">12 Raw CSVs (777 MB)</div>
        </div>
      </div>
    </div>

    <!-- Arrow 1 -> 2 -->
    <div class="arrow-connector">
      <div class="arrow-line"></div>
      <div class="arrow-head"></div>
    </div>

    <!-- STEP 2: DATA CLEANING & ETL -->
    <div class="step-card orange">
      <div class="step-num">2</div>
      <div class="step-body">
        <div class="step-title-row">
          <div class="step-title">PySpark ETL & Imputation</div>
          <span class="step-tag">Distributed Data Prep</span>
        </div>
        <div class="step-desc">
          Executes distributed in-memory data cleaning and structural validation:
          <br>&bull; <strong>Regex Currency Stripping:</strong> Removes symbols ($, &pound;, &euro;, &yen;, commas) and casts price to float double.
          <br>&bull; <strong>Spatial Validation:</strong> Validates WGS84 land coordinates (zero underwater points).
          <br>&bull; <strong>Median Imputation:</strong> Replaces missing review scores with cluster median (<strong>4.5 / 5.0</strong>).
        </div>
        <div class="pills-row">
          <div class="pill highlight">Median Rating: 4.5/5.0</div>
          <div class="pill">Capacity: 2 Guests</div>
          <div class="pill">Price Range: $10 – $3,000 USD</div>
          <div class="pill">Nulls Imputed (Zero Data Loss)</div>
        </div>
      </div>
    </div>

    <!-- Arrow 2 -> 3 -->
    <div class="arrow-connector">
      <div class="arrow-line"></div>
      <div class="arrow-head"></div>
    </div>

    <!-- STEP 3: FEATURE ENGINEERING -->
    <div class="step-card purple">
      <div class="step-num">3</div>
      <div class="step-body">
        <div class="step-title-row">
          <div class="step-title">Feature Engineering & Normalization</div>
          <span class="step-tag">MLlib Transformation</span>
        </div>
        <div class="step-desc">
          Transforms raw heterogeneous fields into standardized mathematical input vectors:
          <br>&bull; <strong>StringIndexer:</strong> Encodes categorical attributes (<span style="font-family: monospace;">city</span> & <span style="font-family: monospace;">room_type</span>) into numeric indices.
          <br>&bull; <strong>Currency Normalization:</strong> Maps prices to standardized USD baseline (<span style="font-family: monospace;">price_usd = price_local * usd_rate</span>).
          <br>&bull; <strong>VectorAssembler:</strong> Merges 6 core features into dense ML vector.
        </div>
        <div class="pills-row">
          <div class="pill highlight">6 Predictive Features</div>
          <div class="pill">accommodates (31.4%)</div>
          <div class="pill">city_idx (22.7%)</div>
          <div class="pill">bedrooms (22.0%)</div>
          <div class="pill">room_idx (11.2%)</div>
        </div>
      </div>
    </div>

    <!-- Arrow 3 -> 4 -->
    <div class="arrow-connector">
      <div class="arrow-line"></div>
      <div class="arrow-head"></div>
    </div>

    <!-- STEP 4: MODEL TRAINING -->
    <div class="step-card indigo">
      <div class="step-num">4</div>
      <div class="step-body">
        <div class="step-title-row">
          <div class="step-title">Distributed MLlib Model Training</div>
          <span class="step-tag">Random Forest Ensemble</span>
        </div>
        <div class="step-desc">
          Trains a distributed non-linear regression ensemble on an <strong>80/20 train-test split</strong>:
          <br>&bull; <strong>Architecture:</strong> 45 parallel decision trees (max depth 9) with 33,955 total decision nodes.
          <br>&bull; <strong>Evaluation vs OLS Baseline:</strong> Achieves <strong>RMSE $209.98 USD (35.1% lower error)</strong> and <strong>R&sup2; = 0.3659 (150% variance gain)</strong>.
          <br>&bull; <strong>Model Serialization:</strong> Exported to 1.7 MB Snappy Parquet metadata.
        </div>
        <div class="pills-row">
          <div class="pill highlight">45 Trees (Depth 9)</div>
          <div class="pill">179,826 Train Records</div>
          <div class="pill">44,272 Test Records</div>
          <div class="pill highlight" style="color: #047857;">&#9660; 35.1% Lower RMSE</div>
          <div class="pill highlight" style="color: #0369A1;">&#9650; 150% Higher R&sup2;</div>
        </div>
      </div>
    </div>

    <!-- Arrow 4 -> 5 -->
    <div class="arrow-connector">
      <div class="arrow-line"></div>
      <div class="arrow-head"></div>
    </div>

    <!-- STEP 5: STORAGE & SERVING -->
    <div class="step-card emerald">
      <div class="step-num">5</div>
      <div class="step-body">
        <div class="step-title-row">
          <div class="step-title">Cassandra Storage & Real-Time Serving</div>
          <span class="step-tag">Sub-15ms Low Latency</span>
        </div>
        <div class="step-desc">
          Delivers sub-millisecond database queries and microsecond tree inferences:
          <br>&bull; <strong>Apache Cassandra NoSQL (Port 9042):</strong> Partitioned keyspaces store 9 macro city aggregates and 14,000 spatial listings (&lt; 3ms query speed).
          <br>&bull; <strong>FastAPI Backend (Port 8001):</strong> Pre-loads Parquet trees for in-memory traversal (<strong>2.18ms latency</strong>) and de-normalizes USD back to local currency (&#8377;, &#165;, &#163;, &#8364;).
          <br>&bull; <strong>React 19 Frontend (Port 5173):</strong> Leaflet marker clustering with <strong>zero DOM lag</strong>.
        </div>
        <div class="pills-row">
          <div class="pill highlight">FastAPI: 2.18ms Latency</div>
          <div class="pill">Cassandra: &lt; 3ms Query</div>
          <div class="pill">14,000 Clustered Pins</div>
          <div class="pill highlight" style="color: #BE123C;">Zero DOM Lag</div>
        </div>
      </div>
    </div>

  </div>

  <div class="footer-note">
    AirIQ Big Data Analytics Laboratory &bull; Department of CSE, Ramdeobaba University (RBU), Nagpur
  </div>

</body>
</html>
"""

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1200, "height": 1650})
        await page.set_content(HTML_CONTENT)
        await page.wait_for_timeout(1000)
        await page.screenshot(path=OUT_DESKTOP)
        await page.screenshot(path=OUT_DESKTOP_ALT)
        await page.screenshot(path=LOCAL_OUT)
        await browser.close()
        print(f"[+] Saved Simple Top-Down Flowchart to: {OUT_DESKTOP}")

if __name__ == "__main__":
    asyncio.run(run())
