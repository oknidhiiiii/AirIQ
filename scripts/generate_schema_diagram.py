import asyncio
from playwright.async_api import async_playwright
import os

OUT_PATH = "/home/adityap/Desktop/cassandra_schema_diagram.png"
LOCAL_OUT = "presentation/charts/cassandra_schema_diagram.png"
os.makedirs("presentation/charts", exist_ok=True)

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'DejaVu Sans', 'Inter', -apple-system, sans-serif; }
  body {
    width: 1400px;
    height: 900px;
    background: #F8FAFC;
    color: #0F172A;
    padding: 36px 44px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
  .header {
    border-bottom: 2px solid #E2E8F0;
    padding-bottom: 16px;
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
  }
  .title {
    font-size: 32px;
    font-weight: 800;
    color: #0F172A;
  }
  .title span { color: #059669; }
  .subtitle {
    font-size: 15px;
    color: #64748B;
    margin-top: 4px;
    font-weight: 500;
  }
  .badges {
    display: flex;
    gap: 10px;
  }
  .badge {
    padding: 6px 14px;
    border-radius: 6px;
    font-size: 13px;
    font-weight: 700;
  }
  .badge.green { background: #DCFCE7; color: #15803D; border: 1.5px solid #BBF7D0; }
  .badge.blue { background: #E0F2FE; color: #0369A1; border: 1.5px solid #BAE6FD; }

  /* Tables Grid */
  .grid {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 24px;
    margin-top: 24px;
    height: 720px;
  }

  .table-card {
    background: #FFFFFF;
    border: 2px solid #CBD5E1;
    border-radius: 12px;
    display: flex;
    flex-direction: column;
    box-shadow: 0 4px 16px rgba(15, 23, 42, 0.05);
    overflow: hidden;
  }
  .table-card.c1 { border-color: #059669; }
  .table-card.c2 { border-color: #0284C7; }
  .table-card.c3 { border-color: #7C3AED; }

  .tbl-header {
    padding: 16px 20px;
    border-bottom: 2px solid #E2E8F0;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .table-card.c1 .tbl-header { background: #F0FDF4; }
  .table-card.c2 .tbl-header { background: #F0F9FF; }
  .table-card.c3 .tbl-header { background: #FAF5FF; }

  .tbl-title {
    font-size: 16.5px;
    font-weight: 800;
    color: #0F172A;
  }
  .tbl-tag {
    font-size: 11px;
    font-weight: 800;
    padding: 3px 8px;
    border-radius: 4px;
    text-transform: uppercase;
  }
  .table-card.c1 .tbl-tag { background: #DCFCE7; color: #15803D; }
  .table-card.c2 .tbl-tag { background: #E0F2FE; color: #0369A1; }
  .table-card.c3 .tbl-tag { background: #F3E8FF; color: #6D28D9; }

  .key-desc {
    padding: 12px 18px;
    background: #F8FAFC;
    border-bottom: 1px solid #E2E8F0;
    font-size: 12px;
    color: #475569;
    line-height: 1.5;
  }
  .key-desc strong { color: #0F172A; }

  .columns-list {
    padding: 14px 18px;
    display: flex;
    flex-direction: column;
    gap: 8px;
    overflow-y: auto;
    font-size: 13px;
  }

  .col-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 4px 8px;
    border-radius: 6px;
    background: #FFFFFF;
    border: 1px solid #F1F5F9;
  }
  .col-row.pk {
    background: #FEF3C7;
    border-color: #FDE68A;
    font-weight: 700;
  }
  .col-row.ck {
    background: #E0F2FE;
    border-color: #BAE6FD;
    font-weight: 700;
  }
  .col-name {
    display: flex;
    align-items: center;
    gap: 6px;
    color: #0F172A;
  }
  .col-type {
    font-family: monospace;
    font-size: 11.5px;
    color: #64748B;
  }
  .badge-pk {
    font-size: 9.5px;
    font-weight: 800;
    background: #D97706;
    color: #FFFFFF;
    padding: 1px 5px;
    border-radius: 3px;
  }
  .badge-ck {
    font-size: 9.5px;
    font-weight: 800;
    background: #0284C7;
    color: #FFFFFF;
    padding: 1px 5px;
    border-radius: 3px;
  }
</style>
</head>
<body>

  <div class="header">
    <div>
      <div class="title">AirIQ: <span>Cassandra NoSQL Database Schema</span></div>
      <div class="subtitle">Keyspace: airbnb_intelligence &bull; SimpleStrategy (Replication Factor = 1) &bull; Port 9042</div>
    </div>
    <div class="badges">
      <div class="badge green">Masterless Wide-Column Ring</div>
      <div class="badge blue">Sub-3ms Read Latency</div>
    </div>
  </div>

  <div class="grid">

    <!-- TABLE 1: listings_by_city -->
    <div class="table-card c2">
      <div class="tbl-header">
        <div class="tbl-title">listings_by_city</div>
        <span class="tbl-tag">Spatial Lookups</span>
      </div>
      <div class="key-desc">
        <strong>Partition Key:</strong> ((country, city))<br>
        <strong>Clustering Key:</strong> listing_id ASC<br>
        <em>All listings for a city sit on the same physical partition node.</em>
      </div>
      <div class="columns-list">
        <div class="col-row pk"><span class="col-name"><span class="badge-pk">PARTITION</span> country</span><span class="col-type">text</span></div>
        <div class="col-row pk"><span class="col-name"><span class="badge-pk">PARTITION</span> city</span><span class="col-type">text</span></div>
        <div class="col-row ck"><span class="col-name"><span class="badge-ck">CLUSTER</span> listing_id</span><span class="col-type">bigint</span></div>
        <div class="col-row"><span class="col-name">name</span><span class="col-type">text</span></div>
        <div class="col-row"><span class="col-name">neighbourhood</span><span class="col-type">text</span></div>
        <div class="col-row"><span class="col-name">latitude</span><span class="col-type">double</span></div>
        <div class="col-row"><span class="col-name">longitude</span><span class="col-type">double</span></div>
        <div class="col-row"><span class="col-name">room_type</span><span class="col-type">text</span></div>
        <div class="col-row"><span class="col-name">property_type</span><span class="col-type">text</span></div>
        <div class="col-row"><span class="col-name">accommodates</span><span class="col-type">int</span></div>
        <div class="col-row"><span class="col-name">bedrooms</span><span class="col-type">double</span></div>
        <div class="col-row"><span class="col-name">bathrooms</span><span class="col-type">double</span></div>
        <div class="col-row"><span class="col-name">price</span><span class="col-type">double</span></div>
        <div class="col-row"><span class="col-name">currency</span><span class="col-type">text</span></div>
        <div class="col-row"><span class="col-name">review_scores_rating</span><span class="col-type">double</span></div>
      </div>
    </div>

    <!-- TABLE 2: listings_by_room_type -->
    <div class="table-card c3">
      <div class="tbl-header">
        <div class="tbl-title">listings_by_room_type</div>
        <span class="tbl-tag">Price Filter Scan</span>
      </div>
      <div class="key-desc">
        <strong>Partition Key:</strong> ((country, city, room_type))<br>
        <strong>Clustering Key:</strong> price DESC, listing_id ASC<br>
        <em>Pre-sorted on disk from highest to lowest price.</em>
      </div>
      <div class="columns-list">
        <div class="col-row pk"><span class="col-name"><span class="badge-pk">PARTITION</span> country</span><span class="col-type">text</span></div>
        <div class="col-row pk"><span class="col-name"><span class="badge-pk">PARTITION</span> city</span><span class="col-type">text</span></div>
        <div class="col-row pk"><span class="col-name"><span class="badge-pk">PARTITION</span> room_type</span><span class="col-type">text</span></div>
        <div class="col-row ck"><span class="col-name"><span class="badge-ck">CLUSTER</span> price (DESC)</span><span class="col-type">double</span></div>
        <div class="col-row ck"><span class="col-name"><span class="badge-ck">CLUSTER</span> listing_id</span><span class="col-type">bigint</span></div>
        <div class="col-row"><span class="col-name">neighbourhood</span><span class="col-type">text</span></div>
        <div class="col-row"><span class="col-name">accommodates</span><span class="col-type">int</span></div>
        <div class="col-row"><span class="col-name">bedrooms</span><span class="col-type">double</span></div>
        <div class="col-row"><span class="col-name">bathrooms</span><span class="col-type">double</span></div>
        <div class="col-row"><span class="col-name">review_scores_rating</span><span class="col-type">double</span></div>
      </div>
    </div>

    <!-- TABLE 3: city_summary_metrics -->
    <div class="table-card c1">
      <div class="tbl-header">
        <div class="tbl-title">city_summary_metrics</div>
        <span class="tbl-tag">Macro Dashboard</span>
      </div>
      <div class="key-desc">
        <strong>Partition Key:</strong> country<br>
        <strong>Clustering Key:</strong> city ASC<br>
        <em>Spark pre-aggregated macro metrics (9 rows).</em>
      </div>
      <div class="columns-list">
        <div class="col-row pk"><span class="col-name"><span class="badge-pk">PARTITION</span> country</span><span class="col-type">text</span></div>
        <div class="col-row ck"><span class="col-name"><span class="badge-ck">CLUSTER</span> city</span><span class="col-type">text</span></div>
        <div class="col-row"><span class="col-name">total_listings</span><span class="col-type">bigint</span></div>
        <div class="col-row"><span class="col-name">avg_price</span><span class="col-type">double</span></div>
        <div class="col-row"><span class="col-name">median_price</span><span class="col-type">double</span></div>
        <div class="col-row"><span class="col-name">min_price</span><span class="col-type">double</span></div>
        <div class="col-row"><span class="col-name">max_price</span><span class="col-type">double</span></div>
        <div class="col-row"><span class="col-name">avg_rating</span><span class="col-type">double</span></div>
        <div class="col-row"><span class="col-name">updated_at</span><span class="col-type">timestamp</span></div>
      </div>
    </div>

  </div>

</body>
</html>
"""

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1400, "height": 900})
        await page.set_content(HTML)
        await page.wait_for_timeout(500)
        await page.screenshot(path=OUT_PATH)
        await page.screenshot(path=LOCAL_OUT)
        await browser.close()
        print(f"[+] Saved Cassandra schema diagram to {OUT_PATH}")

if __name__ == "__main__":
    asyncio.run(run())
