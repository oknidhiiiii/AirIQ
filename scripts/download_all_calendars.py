#!/usr/bin/env python3
"""
scripts/download_all_calendars.py
Downloads the official 365-day calendar datasets (calendar.csv.gz) for all 7 Inside Airbnb cities.
Total download footprint: ~256 MB compressed (~50 Million daily records).
"""

import os
import sys
import time
import urllib.request

CALENDAR_URLS = {
    "amsterdam": "https://data.insideairbnb.com/the-netherlands/north-holland/amsterdam/2026-09-16/data/calendar.csv.gz",
    "sydney": "https://data.insideairbnb.com/australia/nsw/sydney/2026-09-16/data/calendar.csv.gz",
    "new_york": "https://data.insideairbnb.com/united-states/ny/new-york-city/2026-09-14/data/calendar.csv.gz",
    "tokyo": "https://data.insideairbnb.com/japan/kant%C5%8D/tokyo/2026-09-25/data/calendar.csv.gz",
    "rome": "https://data.insideairbnb.com/italy/lazio/rome/2026-09-17/data/calendar.csv.gz",
    "paris": "https://data.insideairbnb.com/france/ile-de-france/paris/2026-09-16/data/calendar.csv.gz",
    "london": "https://data.insideairbnb.com/united-kingdom/england/london/2026-09-17/data/calendar.csv.gz",
}

DEST_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "raw", "calendars"))
os.makedirs(DEST_DIR, exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def download_file(city: str, url: str):
    target_path = os.path.join(DEST_DIR, f"{city}_calendar.csv.gz")
    if os.path.exists(target_path) and os.path.getsize(target_path) > 1024 * 1024:
        size_mb = os.path.getsize(target_path) / (1024 * 1024)
        print(f"[✓] {city.upper()} calendar already downloaded ({size_mb:.2f} MB). Skipping.")
        return target_path

    print(f"[*] Downloading {city.upper()} calendar from {url}...")
    req = urllib.request.Request(url, headers=HEADERS)
    start = time.time()
    with urllib.request.urlopen(req, timeout=120) as response, open(target_path, 'wb') as out_file:
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0
        chunk_size = 1024 * 512  # 512 KB chunks

        while True:
            chunk = response.read(chunk_size)
            if not chunk:
                break
            out_file.write(chunk)
            downloaded += len(chunk)
            if total_size > 0:
                percent = (downloaded / total_size) * 100
                mb = downloaded / (1024 * 1024)
                sys.stdout.write(f"\r    -> {city.upper()}: {mb:.1f} MB / {total_size/(1024*1024):.1f} MB ({percent:.1f}%)")
                sys.stdout.flush()

    elapsed = time.time() - start
    print(f"\n[+] Successfully saved {city.upper()} ({downloaded / (1024*1024):.2f} MB in {elapsed:.1f}s)")
    return target_path

if __name__ == "__main__":
    print("=" * 70)
    print("AirIQ: Inside Airbnb 365-Day Calendar Dataset Downloader")
    print(f"Target Directory: {DEST_DIR}")
    print("=" * 70)

    for city, url in CALENDAR_URLS.items():
        try:
            download_file(city, url)
        except Exception as e:
            print(f"\n[-] Error downloading {city}: {e}")

    print("\n[+] All calendar downloads finished!")
    total_mb = sum(os.path.getsize(os.path.join(DEST_DIR, f)) for f in os.listdir(DEST_DIR)) / (1024*1024)
    print(f"[+] Total Calendar Archive Size on Disk: {total_mb:.2f} MB")
