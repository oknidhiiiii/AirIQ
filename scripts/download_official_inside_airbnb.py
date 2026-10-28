import urllib.request
import os
import gzip
import shutil

# Official verified Inside Airbnb destinations across Europe, North America, and Asia-Pacific
OFFICIAL_CITIES = {
    "paris": {
        "country": "France",
        "city_name": "Paris",
        "currency": "EUR",
        "currency_symbol": "€",
        "url": "https://data.insideairbnb.com/france/ile-de-france/paris/2026-09-16/data/listings.csv.gz"
    },
    "rome": {
        "country": "Italy",
        "city_name": "Rome",
        "currency": "EUR",
        "currency_symbol": "€",
        "url": "https://data.insideairbnb.com/italy/lazio/rome/2026-09-17/data/listings.csv.gz"
    },
    "amsterdam": {
        "country": "Netherlands",
        "city_name": "Amsterdam",
        "currency": "EUR",
        "currency_symbol": "€",
        "url": "https://data.insideairbnb.com/the-netherlands/north-holland/amsterdam/2026-09-16/data/listings.csv.gz"
    },
    "london": {
        "country": "United Kingdom",
        "city_name": "London",
        "currency": "GBP",
        "currency_symbol": "£",
        "url": "https://data.insideairbnb.com/united-kingdom/england/london/2026-09-17/data/listings.csv.gz"
    },
    "tokyo": {
        "country": "Japan",
        "city_name": "Tokyo",
        "currency": "JPY",
        "currency_symbol": "¥",
        "url": "https://data.insideairbnb.com/japan/kant%C5%8D/tokyo/2026-09-25/data/listings.csv.gz"
    },
    "sydney": {
        "country": "Australia",
        "city_name": "Sydney",
        "currency": "AUD",
        "currency_symbol": "A$",
        "url": "https://data.insideairbnb.com/australia/nsw/sydney/2026-09-16/data/listings.csv.gz"
    },
    "new_york": {
        "country": "United States",
        "city_name": "New York City",
        "currency": "USD",
        "currency_symbol": "$",
        "url": "https://data.insideairbnb.com/united-states/ny/new-york-city/2026-09-14/data/listings.csv.gz"
    }
}

RAW_DIR = os.path.abspath("data/raw")
os.makedirs(RAW_DIR, exist_ok=True)

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'Referer': 'https://insideairbnb.com/get-the-data/',
    'Accept': '*/*'
}

for city_key, info in OFFICIAL_CITIES.items():
    gz_target = os.path.join(RAW_DIR, f"{city_key}_listings.csv.gz")
    csv_target = os.path.join(RAW_DIR, f"{city_key}_listings.csv")
    
    if os.path.exists(csv_target) and os.path.getsize(csv_target) > 1000000:
        print(f"[+] {info['city_name']} already downloaded and extracted ({os.path.getsize(csv_target)/1024/1024:.1f} MB)")
        continue
        
    print(f"[*] Downloading {info['city_name']} from Inside Airbnb...")
    req = urllib.request.Request(info['url'], headers=headers)
    with urllib.request.urlopen(req) as resp, open(gz_target, 'wb') as out_f:
        shutil.copyfileobj(resp, out_f)
        
    print(f"    [*] Extracting {gz_target}...")
    with gzip.open(gz_target, 'rb') as f_in, open(csv_target, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
        
    print(f"    [+] Saved {csv_target} ({os.path.getsize(csv_target)/1024/1024:.1f} MB)")
    if os.path.exists(gz_target):
        os.remove(gz_target)

print("[SUCCESS] All official Inside Airbnb global datasets ready.")
