import urllib.request
import os
import gzip
import shutil

CITIES = {
    "paris": {
        "country": "France",
        "city_name": "Paris",
        "url": "https://data.insideairbnb.com/france/ile-de-france/paris/2026-09-16/data/listings.csv.gz"
    },
    "amsterdam": {
        "country": "Netherlands",
        "city_name": "Amsterdam",
        "url": "https://data.insideairbnb.com/the-netherlands/north-holland/amsterdam/2026-09-16/data/listings.csv.gz"
    },
    "rome": {
        "country": "Italy",
        "city_name": "Rome",
        "url": "https://data.insideairbnb.com/italy/lazio/rome/2026-09-17/data/listings.csv.gz"
    },
    "tokyo": {
        "country": "Japan",
        "city_name": "Tokyo",
        "url": "https://data.insideairbnb.com/japan/kantō/tokyo/2026-09-25/data/listings.csv.gz"
    }
}

RAW_DIR = os.path.abspath("data/raw")
os.makedirs(RAW_DIR, exist_ok=True)

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'Referer': 'https://insideairbnb.com/get-the-data/',
    'Accept': '*/*'
}

for city_key, info in CITIES.items():
    gz_target = os.path.join(RAW_DIR, f"{city_key}_listings.csv.gz")
    csv_target = os.path.join(RAW_DIR, f"{city_key}_listings.csv")
    
    if os.path.exists(csv_target):
        print(f"[*] {info['city_name']} CSV already exists at {csv_target}")
        continue
        
    print(f"[*] Downloading {info['city_name']} from Inside Airbnb ({info['url']})...")
    req = urllib.request.Request(info['url'], headers=headers)
    with urllib.request.urlopen(req) as resp, open(gz_target, 'wb') as out_f:
        shutil.copyfileobj(resp, out_f)
    print(f"    [+] Saved {gz_target} ({os.path.getsize(gz_target)/1024/1024:.2f} MB)")
    
    print(f"    [*] Extracting {gz_target} -> {csv_target}...")
    with gzip.open(gz_target, 'rb') as f_in, open(csv_target, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
    print(f"    [+] Extraction complete ({os.path.getsize(csv_target)/1024/1024:.2f} MB)")
    os.remove(gz_target)

print("[SUCCESS] All Inside Airbnb datasets downloaded and extracted.")
