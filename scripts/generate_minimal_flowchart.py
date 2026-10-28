import asyncio
from playwright.async_api import async_playwright
import os

OUT_PATH = "/home/adityap/Desktop/minimal_flowchart.png"

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'DejaVu Sans', 'Inter', -apple-system, sans-serif; }
  body {
    width: 800px;
    height: 1050px;
    background: #FFFFFF;
    color: #0F172A;
    padding: 40px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }
  .title {
    font-size: 28px;
    font-weight: 800;
    color: #0F172A;
    margin-bottom: 36px;
    text-align: center;
  }
  .title span { color: #0284C7; }

  .flow {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 600px;
  }

  .box {
    width: 100%;
    padding: 22px 28px;
    background: #F8FAFC;
    border: 2.5px solid #CBD5E1;
    border-radius: 14px;
    text-align: center;
    font-size: 20px;
    font-weight: 800;
    color: #0F172A;
    box-shadow: 0 4px 14px rgba(15, 23, 42, 0.05);
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 14px;
  }

  .box.c1 { border-color: #0284C7; background: #F0F9FF; color: #0369A1; }
  .box.c2 { border-color: #EA580C; background: #FFF7ED; color: #C2410C; }
  .box.c3 { border-color: #7C3AED; background: #FAF5FF; color: #6D28D9; }
  .box.c4 { border-color: #4F46E5; background: #EEF2FF; color: #4338CA; }
  .box.c5 { border-color: #059669; background: #F0FDF4; color: #047857; }

  .arrow {
    height: 38px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }
  .line {
    width: 3px;
    height: 24px;
    background: #64748B;
  }
  .head {
    width: 0;
    height: 0;
    border-left: 7px solid transparent;
    border-right: 7px solid transparent;
    border-top: 10px solid #64748B;
  }
</style>
</head>
<body>

  <div class="title">AirIQ: <span>System Pipeline Flow</span></div>

  <div class="flow">

    <div class="box c1">1. Data Collection & Ingestion</div>

    <div class="arrow"><div class="line"></div><div class="head"></div></div>

    <div class="box c2">2. PySpark ETL & Cleaning</div>

    <div class="arrow"><div class="line"></div><div class="head"></div></div>

    <div class="box c3">3. Feature Engineering & Normalization</div>

    <div class="arrow"><div class="line"></div><div class="head"></div></div>

    <div class="box c4">4. Distributed MLlib Model Training</div>

    <div class="arrow"><div class="line"></div><div class="head"></div></div>

    <div class="box c5">5. Cassandra Storage & Real-Time Serving</div>

  </div>

</body>
</html>
"""

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 800, "height": 1050})
        await page.set_content(HTML)
        await page.wait_for_timeout(500)
        await page.screenshot(path=OUT_PATH)
        await browser.close()
        print(f"[+] Saved minimal flowchart to {OUT_PATH}")

if __name__ == "__main__":
    asyncio.run(run())
