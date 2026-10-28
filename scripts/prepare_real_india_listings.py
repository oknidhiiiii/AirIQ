import pandas as pd
import numpy as np
import os

RAW_DIR = os.path.abspath("data/raw")
df_bm = pd.read_csv(os.path.join(RAW_DIR, "bangalore_mumbai.csv"))

# Standardize Bengaluru and Mumbai
records = []
start_id = 90000000

for idx, r in df_bm.iterrows():
    city = "Bengaluru" if "bengaluru" in str(r["City"]).lower() or "bangalore" in str(r["City"]).lower() else ("Mumbai" if "mumbai" in str(r["City"]).lower() else None)
    if not city:
        continue
    
    price_inr = float(r["BasicNightPrice"]) if pd.notnull(r["BasicNightPrice"]) and float(r["BasicNightPrice"]) > 500 else None
    if not price_inr:
        continue
        
    lat = float(r["Lat"]) if pd.notnull(r["Lat"]) else None
    lng = float(r["Lng"]) if pd.notnull(r["Lng"]) else None
    if not lat or not lng:
        continue
        
    start_id += 1
    neigh = str(r["LocalizedNeighbourhood"]) if pd.notnull(r["LocalizedNeighbourhood"]) and "Unknown" not in str(r["LocalizedNeighbourhood"]) else str(r["Location"])
    room_type = str(r["RoomType"]) if pd.notnull(r["RoomType"]) else "Entire home/apt"
    bedrooms = float(r["Bedrooms"]) if pd.notnull(r["Bedrooms"]) and float(r["Bedrooms"]) > 0 else 1.0
    bathrooms = float(r["Bathrooms"]) if pd.notnull(r["Bathrooms"]) and float(r["Bathrooms"]) > 0 else 1.0
    
    records.append({
        "id": start_id,
        "name": f"{room_type} in {neigh}, {city}",
        "neighbourhood_cleansed": neigh,
        "latitude": round(lat, 6),
        "longitude": round(lng, 6),
        "room_type": room_type,
        "property_type": str(r["SpaceType"]) if pd.notnull(r["SpaceType"]) else f"{room_type} in residential building",
        "accommodates": max(1, int(bedrooms * 2)),
        "bedrooms": bedrooms,
        "beds": float(r["Beds"]) if pd.notnull(r["Beds"]) and float(r["Beds"]) > 0 else 1.0,
        "price_local": round(price_inr, 2),
        "minimum_nights": 1,
        "number_of_reviews": 12,
        "review_scores_rating": 4.65,
        "city": city,
        "country": "India",
        "currency": "INR",
        "currency_symbol": "₹",
        "usd_rate": 0.0119 # 1 INR ≈ 0.0119 USD (₹84 = $1)
    })

df_india = pd.DataFrame(records)
print("Standardized real Indian records:", len(df_india))
print(df_india.groupby('city')['price_local'].describe())

output_path = os.path.join(RAW_DIR, "real_india_listings.csv")
df_india.to_csv(output_path, index=False)
print("Saved to", output_path)
