import asyncio
from playwright.async_api import async_playwright
import os

OUT_ARCH_DESKTOP = "/home/adityap/Desktop/system_architecture.png"
OUT_ARCH_LIGHT = "/home/adityap/Desktop/system_architecture_light.png"
OUT_PIPE_FLOWCHART = "/home/adityap/Desktop/data_pipeline_flowchart.png"
OUT_PIPE_DESKTOP = "/home/adityap/Desktop/data_pipeline.png"

LOCAL_DIR = "presentation/charts"
os.makedirs(LOCAL_DIR, exist_ok=True)

# ==============================================================================
# 1. LIGHT THEME SYSTEM ARCHITECTURE HTML
# ==============================================================================
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
    background: #F8FAFC;
    color: #0F172A;
    padding: 44px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
  .header {
    border-bottom: 2px solid #E2E8F0;
    padding-bottom: 18px;
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
  }
  .title {
    font-size: 36px;
    font-weight: 800;
    color: #0F172A;
    letter-spacing: -0.5px;
  }
  .title span { color: #E11D48; }
  .subtitle {
    font-size: 16px;
    color: #475569;
    margin-top: 6px;
    font-weight: 500;
  }
  .badge-row {
    display: flex;
    gap: 12px;
  }
  .badge {
    padding: 8px 18px;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 700;
  }
  .badge.coral { color: #BE123C; border: 1.5px solid #FECDD3; background: #FFF1F2; }
  .badge.orange { color: #C2410C; border: 1.5px solid #FED7AA; background: #FFF7ED; }
  .badge.blue { color: #0369A1; border: 1.5px solid #BAE6FD; background: #F0F9FF; }

  /* Main Grid */
  .grid-container {
    display: grid;
    grid-template-columns: 360px 480px 480px 380px;
    gap: 24px;
    height: 870px;
  }
  .tier-col {
    display: flex;
    flex-direction: column;
    gap: 20px;
  }
  .card {
    background: #FFFFFF;
    border: 1.5px solid #E2E8F0;
    border-radius: 14px;
    padding: 24px;
    display: flex;
    flex-direction: column;
    box-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.06);
    position: relative;
  }
  .card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 16px;
    border-bottom: 1.5px solid #F1F5F9;
    padding-bottom: 12px;
  }
  .card-title {
    font-size: 18px;
    font-weight: 800;
    color: #0F172A;
    display: flex;
    align-items: center;
    gap: 10px;
  }
  .tag {
    font-size: 11px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    padding: 4px 10px;
    border-radius: 6px;
  }
  .tag.blue { background: #E0F2FE; color: #0369A1; }
  .tag.orange { background: #FFEDD5; color: #C2410C; }
  .tag.green { background: #DCFCE7; color: #15803D; }
  .tag.rose { background: #FFE4E6; color: #BE123C; }

  .content-list {
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 12px;
    font-size: 13.5px;
    line-height: 1.55;
    color: #334155;
  }
  .content-list li {
    position: relative;
    padding-left: 18px;
  }
  .content-list li::before {
    content: "▶";
    position: absolute;
    left: 0;
    font-size: 9px;
    top: 5px;
    color: #0284C7;
  }
  .tier-col:nth-child(2) .content-list li::before { color: #EA580C; }
  .tier-col:nth-child(3) .content-list li::before { color: #059669; }
  .tier-col:nth-child(4) .content-list li::before { color: #E11D48; }

  .highlight {
    font-weight: 700;
    color: #0F172A;
  }
  .code-inline {
    background: #F1F5F9;
    color: #0F172A;
    padding: 2px 6px;
    border-radius: 4px;
    font-family: monospace;
    font-size: 12px;
    border: 1px solid #E2E8F0;
  }

  .metric-box {
    margin-top: auto;
    background: #F8FAFC;
    border: 1.5px solid #E2E8F0;
    border-radius: 10px;
    padding: 14px 16px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .metric-label {
    font-size: 12.5px;
    color: #64748B;
    font-weight: 600;
  }
  .metric-val {
    font-size: 19px;
    font-weight: 800;
    color: #0F172A;
  }
  .metric-val.emerald { color: #059669; }
  .metric-val.coral { color: #E11D48; }
  .metric-val.blue { color: #0284C7; }

  .connector-text {
    text-align: center;
    font-size: 12px;
    font-weight: 800;
    color: #64748B;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin: 4px 0;
  }
</style>
</head>
<body>

  <div class="header">
    <div>
      <div class="title">AirIQ: <span>Distributed System Architecture</span></div>
      <div class="subtitle">Multi-City Big Data Rental Intelligence Pipeline &bull; Apache Spark 4.2 MLlib + Apache Cassandra 4.1 + React 19 (Light Theme)</div>
    </div>
    <div class="badge-row">
      <div class="badge coral">224,098 Total Records</div>
      <div class="badge orange">Apache Spark MLlib</div>
      <div class="badge blue">Cassandra NoSQL</div>
    </div>
  </div>

  <div class="grid-container">

    <!-- TIER 1: DATA SOURCES -->
    <div class="tier-col">
      <div class="card" style="height: 100%;">
        <div class="card-header">
          <div class="card-title">1. DATA SOURCES</div>
          <span class="tag blue">Raw Ingestion</span>
        </div>
        <ul class="content-list">
          <li style="font-weight: 700; color: #0284C7;">Dual-Dataset Architecture:</li>
          <li><span class="highlight">Official Inside Airbnb (213,264 listings):</span> Quarterly releases covering 7 global hubs (London, Paris, Rome, Tokyo, NYC, Sydney, Amsterdam).</li>
          <li><span class="highlight">DoorStepAnalytics India (10,834 listings):</span> Real scraped listings in INR (&#8377;) covering Mumbai (3,653) & Bengaluru (7,146).</li>
          <li><span class="highlight">Solves Coverage Void:</span> Overcomes Inside Airbnb's total lack of Indian market records.</li>
        </ul>
        <div style="margin-top: 24px; display: flex; flex-direction: column; gap: 12px;">
          <div class="metric-box">
            <span class="metric-label">Global Hubs Volume</span>
            <span class="metric-val blue">213,264</span>
          </div>
          <div class="metric-box">
            <span class="metric-label">Indian Metros Volume</span>
            <span class="metric-val coral">10,834</span>
          </div>
        </div>
      </div>
    </div>

    <!-- TIER 2: SPARK MLLIB ENGINE -->
    <div class="tier-col">
      <div class="card" style="height: 100%;">
        <div class="card-header">
          <div class="card-title">2. SPARK MLlib ENGINE</div>
          <span class="tag orange">Compute (4.2.0)</span>
        </div>
        <ul class="content-list">
          <li style="font-weight: 700; color: #EA580C;">In-Memory Distributed ML:</li>
          <li><span class="highlight">PySpark Cleaning & Casting:</span> Regex price cleaning, null rating median imputation (4.5 / 5.0).</li>
          <li><span class="highlight">Currency Normalization:</span> Standardized baseline (<span class="code-inline">price_usd = price_local * usd_rate</span>) ensures mathematical stability.</li>
          <li><span class="highlight">StringIndexer:</span> Encodes categorical markets & room types into indexed integers.</li>
          <li><span class="highlight">VectorAssembler:</span> Combines 6 features [city, room, capacity, beds, baths, rating].</li>
          <li><span class="highlight">RandomForestRegressor:</span> Trains 45 parallel decision trees (depth 9) on 80% train split.</li>
        </ul>
        <div style="margin-top: auto; display: flex; flex-direction: column; gap: 12px;">
          <div class="metric-box">
            <span class="metric-label">Test Split RMSE</span>
            <span class="metric-val emerald">$209.98 USD</span>
          </div>
          <div class="metric-box">
            <span class="metric-label">Error Reduction vs OLS</span>
            <span class="metric-val emerald">&#9660; 35.1%</span>
          </div>
        </div>
      </div>
    </div>

    <!-- TIER 3: CASSANDRA & API -->
    <div class="tier-col">
      <div class="card" style="height: 100%;">
        <div class="card-header">
          <div class="card-title">3. CASSANDRA & API</div>
          <span class="tag green">Storage & Serving</span>
        </div>
        <ul class="content-list">
          <li style="font-weight: 700; color: #059669;">Distributed Storage & API:</li>
          <li><span class="highlight">Apache Cassandra 4.1.0 (Port 9042):</span> Masterless wide-column ring for high-availability spatial writes.</li>
          <li><span class="highlight">Keyspace Partitioning:</span> Table <span class="code-inline">city_summary_metrics</span> partitioned by country; table <span class="code-inline">listings_by_city</span> partitioned by (country, city).</li>
          <li><span class="highlight">FastAPI Microservice (Port 8001):</span> Asynchronous non-blocking Python ASGI server.</li>
          <li><span class="highlight">In-Memory Tree Traversal:</span> Pre-loads 45 Spark Parquet trees for live inference in &lt; 15ms.</li>
          <li><span class="highlight">Currency De-normalization:</span> Dynamically maps base USD prediction back into native local currency (&#8377;, &#165;, &#163;, &#8364;).</li>
        </ul>
        <div style="margin-top: auto; display: flex; flex-direction: column; gap: 12px;">
          <div class="metric-box">
            <span class="metric-label">Prediction Latency</span>
            <span class="metric-val emerald">&lt; 15 ms</span>
          </div>
          <div class="metric-box">
            <span class="metric-label">Cassandra Query Speed</span>
            <span class="metric-val emerald">&lt; 3 ms</span>
          </div>
        </div>
      </div>
    </div>

    <!-- TIER 4: CLIENT UI -->
    <div class="tier-col">
      <div class="card" style="height: 100%;">
        <div class="card-header">
          <div class="card-title">4. CLIENT UI</div>
          <span class="tag rose">React 19 + Vite</span>
        </div>
        <ul class="content-list">
          <li style="font-weight: 700; color: #BE123C;">Geospatial & Analytics UI:</li>
          <li><span class="highlight">React 19 SPA (Port 5173):</span> Responsive component architecture built with Tailwind CSS.</li>
          <li><span class="highlight">Leaflet Marker Clustering:</span> Dynamically aggregates dense pins into clickable badges; eliminates DOM lag.</li>
          <li><span class="highlight">Zero Blurry Heatmaps:</span> Transparent pin inspection showing exact neighborhood, price, and rating.</li>
          <li><span class="highlight">Verified Land Coordinates:</span> 14,000 spatial pins checked within legitimate land boundaries.</li>
          <li><span class="highlight">Native Currency UI:</span> Displays &#8377; INR, &#165; JPY, &#163; GBP, &#8364; EUR, A$ AUD, and $ USD.</li>
        </ul>
        <div style="margin-top: auto; display: flex; flex-direction: column; gap: 12px;">
          <div class="metric-box">
            <span class="metric-label">Markets Supported</span>
            <span class="metric-val coral">9 Cities</span>
          </div>
          <div class="metric-box">
            <span class="metric-label">DOM Performance</span>
            <span class="metric-val blue">Zero Lag (Clustered)</span>
          </div>
        </div>
      </div>
    </div>

  </div>

</body>
</html>
"""

# ==============================================================================
# 2. LIGHT THEME DATA PIPELINE FLOWCHART HTML (PERFECTLY ALIGNED)
# ==============================================================================
FLOWCHART_HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'DejaVu Sans', 'Inter', -apple-system, sans-serif; }
  body {
    width: 1920px;
    height: 1080px;
    background: #F8FAFC;
    color: #0F172A;
    padding: 34px 44px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
  .header {
    border-bottom: 2px solid #E2E8F0;
    padding-bottom: 14px;
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
  }
  .title {
    font-size: 35px;
    font-weight: 800;
    color: #0F172A;
    letter-spacing: -0.5px;
  }
  .title span { color: #0284C7; }
  .subtitle {
    font-size: 15px;
    color: #475569;
    margin-top: 4px;
    font-weight: 500;
  }
  .badge-row {
    display: flex;
    gap: 12px;
  }
  .badge {
    padding: 7px 16px;
    border-radius: 8px;
    font-size: 13.5px;
    font-weight: 700;
  }
  .badge.blue { color: #0369A1; border: 1.5px solid #BAE6FD; background: #F0F9FF; }
  .badge.orange { color: #C2410C; border: 1.5px solid #FED7AA; background: #FFF7ED; }
  .badge.green { color: #15803D; border: 1.5px solid #BBF7D0; background: #F0FDF4; }

  /* Flowchart Canvas */
  .canvas {
    height: 900px;
    position: relative;
    background: #FFFFFF;
    border: 1.5px solid #E2E8F0;
    border-radius: 16px;
    box-shadow: 0 4px 24px -2px rgba(15, 23, 42, 0.07);
    padding: 24px;
  }

  /* SVG overlay for connecting lines */
  svg.connectors {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 1;
  }

  /* Node styling */
  .node {
    position: absolute;
    background: #FFFFFF;
    border: 2px solid #CBD5E1;
    border-radius: 12px;
    padding: 14px 18px;
    box-shadow: 0 4px 14px rgba(15, 23, 42, 0.06);
    z-index: 2;
    display: flex;
    flex-direction: column;
  }
  .node.blue { border-color: #0284C7; background: #F0F9FF; }
  .node.orange { border-color: #EA580C; background: #FFF7ED; }
  .node.purple { border-color: #7C3AED; background: #FAF5FF; }
  .node.green { border-color: #059669; background: #F0FDF4; }
  .node.rose { border-color: #E11D48; background: #FFF1F2; }

  .node-title {
    font-size: 13.5px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .node.blue .node-title { color: #0369A1; }
  .node.orange .node-title { color: #C2410C; }
  .node.purple .node-title { color: #6D28D9; }
  .node.green .node-title { color: #047857; }
  .node.rose .node-title { color: #BE123C; }

  .node-desc {
    font-size: 12px;
    color: #334155;
    line-height: 1.5;
  }
  .node-desc strong { color: #0F172A; }

  /* Decision Diamond */
  .diamond {
    position: absolute;
    width: 140px;
    height: 140px;
    background: #FEF3C7;
    border: 2px solid #D97706;
    transform: rotate(45deg);
    z-index: 2;
    box-shadow: 0 4px 12px rgba(217, 119, 6, 0.15);
  }
  .diamond-inner {
    position: absolute;
    width: 140px;
    height: 140px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 10px;
    transform: rotate(-45deg);
    z-index: 3;
    pointer-events: none;
  }
  .diamond-title {
    font-size: 11px;
    font-weight: 800;
    color: #92400E;
    text-transform: uppercase;
    line-height: 1.25;
  }

  /* Stage Headers */
  .stage-badge {
    position: absolute;
    font-size: 10.5px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    padding: 3px 8px;
    border-radius: 5px;
    z-index: 3;
    top: -10px;
    left: 14px;
  }
  .stage-badge.blue { background: #0284C7; color: #FFFFFF; }
  .stage-badge.orange { background: #EA580C; color: #FFFFFF; }
  .stage-badge.purple { background: #7C3AED; color: #FFFFFF; }
  .stage-badge.green { background: #059669; color: #FFFFFF; }
  .stage-badge.rose { background: #E11D48; color: #FFFFFF; }

  /* Flow text markers */
  .flow-label {
    font-size: 11px;
    font-weight: 800;
    fill: #0F172A;
  }
  .flow-label.blue { fill: #0369A1; }
  .flow-label.orange { fill: #C2410C; }
  .flow-label.purple { fill: #6D28D9; }
  .flow-label.green { fill: #047857; }

  /* Legend & Footnotes */
  .flowchart-footer {
    position: absolute;
    bottom: 12px;
    left: 28px;
    right: 28px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 1.5px solid #F1F5F9;
    padding-top: 10px;
    font-size: 12px;
    color: #64748B;
    font-weight: 600;
  }
  .legend {
    display: flex;
    gap: 18px;
  }
  .legend-item {
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .legend-dot {
    width: 10px;
    height: 10px;
    border-radius: 3px;
  }
</style>
</head>
<body>

  <div class="header">
    <div>
      <div class="title">AirIQ: <span>End-to-End Data & ML Pipeline Flowchart</span></div>
      <div class="subtitle">Complete Data Flow: Dual-Source Ingestion &rarr; PySpark ETL &rarr; MLlib Random Forest &rarr; Cassandra Sink &rarr; FastAPI Serving</div>
    </div>
    <div class="badge-row">
      <div class="badge blue">224,098 Total Records</div>
      <div class="badge orange">45 Spark Trees (Depth 9)</div>
      <div class="badge green">2.18ms Serving Latency</div>
    </div>
  </div>

  <div class="canvas">

    <!-- SVG Connectors -->
    <svg class="connectors">
      <defs>
        <marker id="arrow" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 0 1 L 10 5 L 0 9 z" fill="#64748B" />
        </marker>
        <marker id="arrow-blue" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 0 1 L 10 5 L 0 9 z" fill="#0284C7" />
        </marker>
        <marker id="arrow-orange" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 0 1 L 10 5 L 0 9 z" fill="#EA580C" />
        </marker>
        <marker id="arrow-green" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 0 1 L 10 5 L 0 9 z" fill="#059669" />
        </marker>
        <marker id="arrow-purple" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 0 1 L 10 5 L 0 9 z" fill="#7C3AED" />
        </marker>
        <marker id="arrow-rose" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 0 1 L 10 5 L 0 9 z" fill="#E11D48" />
        </marker>
      </defs>

      <!-- 1. Sources to Ingestion -->
      <path d="M 250 125 L 300 180" stroke="#0284C7" stroke-width="2.5" fill="none" marker-end="url(#arrow-blue)" />
      <path d="M 250 265 L 300 215" stroke="#0284C7" stroke-width="2.5" fill="none" marker-end="url(#arrow-blue)" />

      <!-- 2. Ingestion to ETL Clean -->
      <path d="M 500 197 L 550 197" stroke="#EA580C" stroke-width="2.5" fill="none" marker-end="url(#arrow-orange)" />

      <!-- 3. ETL Clean to Diamond Decision -->
      <path d="M 760 197 L 810 197" stroke="#EA580C" stroke-width="2.5" fill="none" marker-end="url(#arrow-orange)" />

      <!-- 4. Diamond Decision Paths -->
      <!-- YES: Null -> Down to Impute Medians -->
      <path d="M 880 267 L 880 310" stroke="#D97706" stroke-width="2.5" fill="none" marker-end="url(#arrow)" />
      <text x="890" y="292" class="flow-label orange">YES (Null)</text>

      <!-- NO: Clean -> Direct to StringIndexer & VectorAssembler -->
      <path d="M 950 197 L 1020 197" stroke="#059669" stroke-width="2.5" fill="none" marker-end="url(#arrow-green)" />
      <text x="955" y="172" class="flow-label green">NO (Clean)</text>

      <!-- Impute Medians -> StringIndexer & VectorAssembler -->
      <path d="M 970 367 L 1070 367 L 1070 270" stroke="#D97706" stroke-width="2.5" fill="none" marker-end="url(#arrow)" />

      <!-- 5. VectorAssembler to 80/20 Train-Test Split -->
      <path d="M 1240 200 L 1300 200" stroke="#7C3AED" stroke-width="2.5" fill="none" marker-end="url(#arrow-purple)" />

      <!-- 6. Split to 80% Train Model -->
      <path d="M 1440 185 L 1480 185 L 1480 135 L 1520 135" stroke="#7C3AED" stroke-width="2.5" fill="none" marker-end="url(#arrow-purple)" />
      <text x="1448" y="160" class="flow-label purple">80% Train</text>

      <!-- 7. Split to 20% Evaluate Model -->
      <path d="M 1440 215 L 1480 215 L 1480 417 L 1520 417" stroke="#64748B" stroke-width="2.5" fill="none" marker-end="url(#arrow)" />
      <text x="1448" y="240" class="flow-label">20% Test</text>

      <!-- 8. Train Model to Snappy Parquet -->
      <path d="M 1645 195 L 1645 225" stroke="#7C3AED" stroke-width="2.5" fill="none" marker-end="url(#arrow-purple)" />

      <!-- 9. ETL Cleansed Master Data -> Cassandra Sink -->
      <path d="M 1150 270 L 1150 490 L 1205 490 L 1205 580" stroke="#059669" stroke-width="2.5" fill="none" marker-end="url(#arrow-green)" />
      <text x="1160" y="465" class="flow-label green" style="font-size: 11.5px;">Bulk Sink: 14k Spatial + 9 City Aggregates</text>

      <!-- 10. Serialized Parquet Model -> FastAPI Microservice In-Memory (routes around Model Evaluation card) -->
      <path d="M 1750 280 L 1785 280 L 1785 530 L 730 530 L 730 580" stroke="#7C3AED" stroke-width="2.5" fill="none" marker-end="url(#arrow-purple)" />
      <text x="1350" y="520" class="flow-label purple" style="font-size: 11.5px;">Pre-load 45 Trees to In-Memory Struct</text>


      <!-- 11. Cassandra to FastAPI Serving Queries -->
      <path d="M 1040 665 L 900 665" stroke="#059669" stroke-width="2.5" fill="none" marker-end="url(#arrow-green)" />
      <text x="918" y="655" class="flow-label green">CQL Queries (&lt;3ms)</text>

      <!-- 12. FastAPI to React Client UI -->
      <path d="M 560 665 L 420 665" stroke="#E11D48" stroke-width="2.5" fill="none" marker-end="url(#arrow-rose)" />
      <text x="432" y="655" class="flow-label" style="fill: #BE123C;">Sub-15ms REST JSON</text>
    </svg>

    <!-- ROW 1: INGESTION & TRAINING -->

    <!-- Source A -->
    <div class="node blue" style="top: 70px; left: 30px; width: 220px; height: 110px;">
      <span class="stage-badge blue">Step 01: Data Collection</span>
      <div class="node-title">&#128196; Inside Airbnb</div>
      <div class="node-desc">
        <strong>213,264 Global Listings</strong><br>
        7 Hubs: London, Paris, Rome, Tokyo, NYC, Sydney, Amsterdam.
      </div>
    </div>

    <!-- Source B -->
    <div class="node blue" style="top: 210px; left: 30px; width: 220px; height: 110px;">
      <span class="stage-badge blue">Step 01: Data Collection</span>
      <div class="node-title">&#128196; DoorStepAnalytics</div>
      <div class="node-desc">
        <strong>10,834 Real Indian Listings</strong><br>
        Mumbai (3,653) &amp; Bengaluru (7,146) in authentic INR (&#8377;).
      </div>
    </div>

    <!-- Stage 01: Ingestion -->
    <div class="node orange" style="top: 135px; left: 300px; width: 200px; height: 125px;">
      <span class="stage-badge orange">Step 01: Ingestion</span>
      <div class="node-title">&#9881; Spark Ingestion</div>
      <div class="node-desc">
        Multi-line CSV parser<br>
        Header normalization<br>
        <strong>224,098 Total Records</strong>
      </div>
    </div>

    <!-- Stage 02: PySpark ETL -->
    <div class="node orange" style="top: 135px; left: 550px; width: 210px; height: 125px;">
      <span class="stage-badge orange">Step 02: Cleaning</span>
      <div class="node-title">&#128295; PySpark ETL Clean</div>
      <div class="node-desc">
        Regex symbol stripping<br>
        Double casting for coords<br>
        <strong>price_usd = price * rate</strong>
      </div>
    </div>

    <!-- Diamond Decision -->
    <div class="diamond" style="top: 127px; left: 810px;"></div>
    <div class="diamond-inner" style="top: 127px; left: 810px;">
      <div class="diamond-title">Null Rating<br>or Capacity?</div>
    </div>

    <!-- Impute Medians (Below Diamond) -->
    <div class="node orange" style="top: 310px; left: 790px; width: 180px; height: 115px;">
      <span class="stage-badge orange">Step 02: Imputation</span>
      <div class="node-title">&#129690; Impute Medians</div>
      <div class="node-desc">
        Rating &larr; <strong>4.5 / 5.0</strong><br>
        Capacity &larr; <strong>2 guests</strong><br>
        Bedrooms &larr; <strong>1.0</strong>
      </div>
    </div>

    <!-- Stage 03: Feature Engineering -->
    <div class="node purple" style="top: 135px; left: 1020px; width: 220px; height: 135px;">
      <span class="stage-badge purple">Step 03: Feature Eng.</span>
      <div class="node-title">&#128736; StringIndexer &amp; Vector</div>
      <div class="node-desc">
        Encode <strong>city</strong> &amp; <strong>room_type</strong><br>
        VectorAssembler merges 6 continuous/categorical inputs.
      </div>
    </div>

    <!-- 80/20 Train-Test Split Node -->
    <div class="node purple" style="top: 145px; left: 1300px; width: 140px; height: 110px; text-align: center; justify-content: center;">
      <div class="node-title" style="justify-content: center;">80 / 20 Split</div>
      <div class="node-desc" style="font-weight: 700;">seed = 42</div>
    </div>

    <!-- 80% Train Model -->
    <div class="node purple" style="top: 75px; left: 1520px; width: 230px; height: 120px;">
      <span class="stage-badge purple">Step 04: Training</span>
      <div class="node-title">&#129302; MLlib Random Forest</div>
      <div class="node-desc">
        <strong>179,826 Train Records</strong><br>
        45 Trees, Max Depth = 9<br>
        Variance reduction criterion
      </div>
    </div>

    <!-- Snappy Parquet Serialized Model -->
    <div class="node purple" style="top: 225px; left: 1520px; width: 230px; height: 110px; background: #FAF5FF; border-color: #7C3AED;">
      <div class="node-title" style="color: #6D28D9;">&#128190; Snappy Parquet</div>
      <div class="node-desc">
        1.7 MB serialized model<br>
        <strong>33,955 Decision Nodes</strong>
      </div>
    </div>

    <!-- 20% Evaluate Model -->
    <div class="node" style="top: 360px; left: 1520px; width: 230px; height: 115px; border-color: #64748B; background: #F8FAFC;">
      <span class="stage-badge" style="background: #475569; color: #fff;">Step 04: Evaluation</span>
      <div class="node-title" style="color: #475569;">&#128202; Model Evaluation</div>
      <div class="node-desc">
        <strong>44,272 Test Records</strong><br>
        RMSE: <strong>$209.98</strong> (35% lower)<br>
        R&sup2;: <strong>0.3659</strong> (150% gain)
      </div>
    </div>

    <!-- ROW 2: SINK, SERVING & CLIENT -->

    <!-- Cassandra Sink -->
    <div class="node green" style="top: 580px; left: 1040px; width: 330px; height: 165px;">
      <span class="stage-badge green">Step 05: Cassandra Sink</span>
      <div class="node-title">&#128452; Apache Cassandra (9042)</div>
      <div class="node-desc">
        <strong>city_summary_metrics:</strong> 9 macro rows (partition: country, cluster: city)<br>
        <strong>listings_by_city:</strong> 14,000 spatial pins<br>
        Masterless wide-column ring (latency &lt; 3ms)
      </div>
    </div>

    <!-- FastAPI Backend -->
    <div class="node green" style="top: 580px; left: 560px; width: 340px; height: 165px;">
      <span class="stage-badge green">Step 05: Serving API</span>
      <div class="node-title">&#9889; FastAPI Microservice (8001)</div>
      <div class="node-desc">
        In-memory 45-tree traversal (<strong>2.18ms latency</strong>)<br>
        Dynamic currency de-normalization (&#8377;, &#165;, &#163;, &#8364;)<br>
        Non-blocking ASGI Python 3.14
      </div>
    </div>

    <!-- React Client UI -->
    <div class="node rose" style="top: 580px; left: 80px; width: 340px; height: 165px;">
      <span class="stage-badge rose">Step 05: Client UI</span>
      <div class="node-title">&#128187; React 19 + Leaflet UI (5173)</div>
      <div class="node-desc">
        Dynamic Leaflet marker clustering (<strong>zero DOM lag</strong>)<br>
        Real-time price prediction sliders &amp; bounds<br>
        Macro city economic intelligence cards
      </div>
    </div>


    <!-- Flowchart Footer / Legend -->
    <div class="flowchart-footer">
      <div class="legend">
        <div class="legend-item"><div class="legend-dot" style="background: #0284C7;"></div> Ingestion &amp; Raw Sources</div>
        <div class="legend-item"><div class="legend-dot" style="background: #EA580C;"></div> PySpark ETL &amp; Cleaning</div>
        <div class="legend-item"><div class="legend-dot" style="background: #D97706;"></div> Conditional Imputation</div>
        <div class="legend-item"><div class="legend-dot" style="background: #7C3AED;"></div> MLlib Random Forest Training</div>
        <div class="legend-item"><div class="legend-dot" style="background: #059669;"></div> Cassandra &amp; Serving Engine</div>
        <div class="legend-item"><div class="legend-dot" style="background: #E11D48;"></div> React UI Presentation</div>
      </div>
      <div>AirIQ Big Data Analytics Laboratory &bull; Ramdeobaba University (RBU)</div>
    </div>

  </div>

</body>
</html>
"""


async def generate():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        # 1. Generate Light System Architecture
        page = await browser.new_page(viewport={"width": 1920, "height": 1080})
        await page.set_content(ARCH_HTML)
        await page.wait_for_timeout(1000)
        await page.screenshot(path=OUT_ARCH_DESKTOP)
        await page.screenshot(path=OUT_ARCH_LIGHT)
        await page.screenshot(path=os.path.join(LOCAL_DIR, "system_architecture_light.png"))
        print(f"[+] Saved Light System Architecture to: {OUT_ARCH_DESKTOP}")
        
        # 2. Generate Light Data Pipeline Flowchart
        page_pipe = await browser.new_page(viewport={"width": 1920, "height": 1080})
        await page_pipe.set_content(FLOWCHART_HTML)
        await page_pipe.wait_for_timeout(1000)
        await page_pipe.screenshot(path=OUT_PIPE_FLOWCHART)
        await page_pipe.screenshot(path=OUT_PIPE_DESKTOP)
        await page_pipe.screenshot(path=os.path.join(LOCAL_DIR, "data_pipeline_flowchart.png"))
        print(f"[+] Saved Light Data Pipeline Flowchart to: {OUT_PIPE_FLOWCHART}")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(generate())
