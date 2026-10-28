import urllib.request
import os
import pandas as pd

RAW_DIR = os.path.abspath("data/raw")
os.makedirs(RAW_DIR, exist_ok=True)

URLS = {
    "bangalore_mumbai": "https://raw.githubusercontent.com/reejariyaz/Comparative-Analysis-of-Airbnb-Market-Trends-Bangalore-Mumbai/main/cleaned_dataset.csv",
    "india_gems": "https://raw.githubusercontent.com/DivyaBasantray/India-s-Airbnb-Gems-Project/main/airbnb_clean.csv"
}

for name, url in URLS.items():
    target = os.path.join(RAW_DIR, f"{name}.csv")
    print(f"[*] Downloading real Indian Airbnb dataset from {url}...")
    urllib.request.urlretrieve(url, target)
    print(f"    [+] Saved to {target} ({os.path.getsize(target)/1024/1024:.2f} MB)")

df_bm = pd.read_csv(os.path.join(RAW_DIR, "bangalore_mumbai.csv"))
print("Bangalore & Mumbai Shape:", df_bm.shape)
print("BM Columns:", df_bm.columns.tolist()[:12])
print("BM City value counts:")
print(df_bm['City'].value_counts() if 'City' in df_bm.columns else "No City col")

df_gems = pd.read_csv(os.path.join(RAW_DIR, "india_gems.csv"))
print("India Gems Shape:", df_gems.shape)
print("Gems Columns:", df_gems.columns.tolist()[:12])
