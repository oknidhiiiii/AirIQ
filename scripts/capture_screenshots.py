import asyncio
from playwright.async_api import async_playwright
import os

PAGES = [
    ("dashboard", "http://localhost:5173/"),
    ("prediction", "http://localhost:5173/predict"),
    ("explorer", "http://localhost:5173/explore"),
    ("evaluation", "http://localhost:5173/evaluation"),
    ("swagger_docs", "http://127.0.0.1:8001/docs")
]

OUT_DIR = "/home/adityap/Desktop/PR/BDALAB/airbnb-price-intelligence/presentation/screenshots"

async def capture():
    os.makedirs(OUT_DIR, exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            executable_path="/usr/bin/google-chrome",
            args=["--no-sandbox", "--disable-setuid-sandbox"]
        )
        context = await browser.new_context(viewport={"width": 1440, "height": 900})
        page = await context.new_page()

        for name, url in PAGES:
            print(f"Navigating to {url}...")
            await page.goto(url, wait_until="networkidle")
            await asyncio.sleep(2)  # Allow charts / leaflet tiles to stabilize
            
            # Specific interactions
            if name == "prediction":
                # Click calculate to show predicted card
                calc_btn = page.locator("button:has-text('Calculate')")
                if await calc_btn.count() > 0:
                    await calc_btn.first.click()
                    await asyncio.sleep(1)
            elif name == "explorer":
                await asyncio.sleep(3)  # Map tiles rendering
                
            path = os.path.join(OUT_DIR, f"{name}.png")
            await page.screenshot(path=path, full_page=False)
            print(f"Saved screenshot: {path}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(capture())
