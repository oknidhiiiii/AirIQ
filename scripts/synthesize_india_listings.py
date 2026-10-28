import csv
import random
import os

NEIGHBOURHOOD_POLYGONS = {
    "Mumbai": {
        "state": "Maharashtra",
        "base_inr": 4200,
        "count": 5500,
        "neighbourhoods": [
            {"name": "Bandra West", "lat": 19.0596, "lng": 72.8295, "radius": 0.012},
            {"name": "Bandra East / BKC", "lat": 19.0660, "lng": 72.8680, "radius": 0.012},
            {"name": "Juhu", "lat": 19.1075, "lng": 72.8263, "radius": 0.010},
            {"name": "Andheri West", "lat": 19.1363, "lng": 72.8277, "radius": 0.015},
            {"name": "Andheri East", "lat": 19.1136, "lng": 72.8697, "radius": 0.015},
            {"name": "Powai", "lat": 19.1176, "lng": 72.9060, "radius": 0.015},
            {"name": "Colaba", "lat": 18.9067, "lng": 72.8147, "radius": 0.008},
            {"name": "Worli", "lat": 19.0134, "lng": 72.8184, "radius": 0.009},
            {"name": "Dadar", "lat": 19.0178, "lng": 72.8478, "radius": 0.012},
            {"name": "Santacruz", "lat": 19.0843, "lng": 72.8360, "radius": 0.010},
            {"name": "Lower Parel", "lat": 18.9950, "lng": 72.8300, "radius": 0.010},
            {"name": "Khar West", "lat": 19.0700, "lng": 72.8340, "radius": 0.008}
        ]
    },
    "Delhi NCR": {
        "state": "Delhi",
        "base_inr": 3100,
        "count": 5000,
        "neighbourhoods": [
            {"name": "Hauz Khas", "lat": 28.5494, "lng": 77.2001, "radius": 0.012},
            {"name": "Connaught Place", "lat": 28.6315, "lng": 77.2167, "radius": 0.012},
            {"name": "South Extension", "lat": 28.5714, "lng": 77.2209, "radius": 0.012},
            {"name": "Vasant Kunj", "lat": 28.5244, "lng": 77.1557, "radius": 0.015},
            {"name": "Saket", "lat": 28.5244, "lng": 77.2100, "radius": 0.012},
            {"name": "Greater Kailash", "lat": 28.5414, "lng": 77.2389, "radius": 0.012},
            {"name": "Dwarka", "lat": 28.5921, "lng": 77.0460, "radius": 0.020},
            {"name": "Defence Colony", "lat": 28.5733, "lng": 77.2341, "radius": 0.010},
            {"name": "Karol Bagh", "lat": 28.6517, "lng": 77.1906, "radius": 0.012},
            {"name": "Lajpat Nagar", "lat": 28.5677, "lng": 77.2433, "radius": 0.012}
        ]
    },
    "Bengaluru": {
        "state": "Karnataka",
        "base_inr": 3400,
        "count": 4800,
        "neighbourhoods": [
            {"name": "Koramangala", "lat": 12.9352, "lng": 77.6245, "radius": 0.015},
            {"name": "Indiranagar", "lat": 12.9719, "lng": 77.6412, "radius": 0.015},
            {"name": "Whitefield", "lat": 12.9698, "lng": 77.7499, "radius": 0.020},
            {"name": "HSR Layout", "lat": 12.9121, "lng": 77.6446, "radius": 0.015},
            {"name": "JP Nagar", "lat": 12.9063, "lng": 77.5857, "radius": 0.015},
            {"name": "MG Road", "lat": 12.9756, "lng": 77.6066, "radius": 0.010},
            {"name": "Electronic City", "lat": 12.8399, "lng": 77.6770, "radius": 0.020},
            {"name": "Bellandur", "lat": 12.9260, "lng": 77.6762, "radius": 0.015},
            {"name": "Marathahalli", "lat": 12.9591, "lng": 77.6974, "radius": 0.015},
            {"name": "Jayanagar", "lat": 12.9308, "lng": 77.5838, "radius": 0.015}
        ]
    },
    "Goa": {
        "state": "Goa",
        "base_inr": 5200,
        "count": 5200,
        "neighbourhoods": [
            {"name": "Anjuna", "lat": 15.5866, "lng": 73.7436, "radius": 0.009},
            {"name": "Calangute", "lat": 15.5449, "lng": 73.7553, "radius": 0.009},
            {"name": "Baga", "lat": 15.5553, "lng": 73.7517, "radius": 0.008},
            {"name": "Candolim", "lat": 15.5178, "lng": 73.7686, "radius": 0.009},
            {"name": "Panaji", "lat": 15.4909, "lng": 73.8278, "radius": 0.012},
            {"name": "Vagator", "lat": 15.6028, "lng": 73.7445, "radius": 0.008},
            {"name": "Morjim", "lat": 15.6294, "lng": 73.7441, "radius": 0.008},
            {"name": "Assagao", "lat": 15.5947, "lng": 73.7749, "radius": 0.012},
            {"name": "Siolim", "lat": 15.6267, "lng": 73.7725, "radius": 0.012},
            {"name": "Palolem", "lat": 15.0100, "lng": 74.0232, "radius": 0.009}
        ]
    },
    "Jaipur": {
        "state": "Rajasthan",
        "base_inr": 2800,
        "count": 3500,
        "neighbourhoods": [
            {"name": "C-Scheme", "lat": 26.9094, "lng": 75.8016, "radius": 0.012},
            {"name": "Malviya Nagar", "lat": 26.8528, "lng": 75.8236, "radius": 0.015},
            {"name": "Vaishali Nagar", "lat": 26.9042, "lng": 75.7441, "radius": 0.015},
            {"name": "Civil Lines", "lat": 26.9067, "lng": 75.7865, "radius": 0.012},
            {"name": "Mansarovar", "lat": 26.8570, "lng": 75.7659, "radius": 0.015},
            {"name": "Bani Park", "lat": 26.9272, "lng": 75.7923, "radius": 0.012},
            {"name": "Raja Park", "lat": 26.8973, "lng": 75.8274, "radius": 0.012},
            {"name": "Amer", "lat": 26.9855, "lng": 75.8513, "radius": 0.012}
        ]
    },
    "Hyderabad": {
        "state": "Telangana",
        "base_inr": 2900,
        "count": 3800,
        "neighbourhoods": [
            {"name": "Banjara Hills", "lat": 17.4156, "lng": 78.4357, "radius": 0.015},
            {"name": "Jubilee Hills", "lat": 17.4319, "lng": 78.4073, "radius": 0.015},
            {"name": "Gachibowli", "lat": 17.4401, "lng": 78.3489, "radius": 0.018},
            {"name": "Hitec City", "lat": 17.4474, "lng": 78.3762, "radius": 0.015},
            {"name": "Madhapur", "lat": 17.4483, "lng": 78.3915, "radius": 0.015},
            {"name": "Kondapur", "lat": 17.4699, "lng": 78.3578, "radius": 0.015},
            {"name": "Begumpet", "lat": 17.4447, "lng": 78.4664, "radius": 0.012},
            {"name": "Kukatpally", "lat": 17.4947, "lng": 78.3996, "radius": 0.018}
        ]
    },
    "Kolkata": {
        "state": "West Bengal",
        "base_inr": 2400,
        "count": 3200,
        "neighbourhoods": [
            {"name": "Park Street", "lat": 22.5513, "lng": 88.3524, "radius": 0.010},
            {"name": "Salt Lake", "lat": 22.5867, "lng": 88.4178, "radius": 0.018},
            {"name": "New Town", "lat": 22.5958, "lng": 88.4795, "radius": 0.020},
            {"name": "Ballygunge", "lat": 22.5280, "lng": 88.3653, "radius": 0.012},
            {"name": "Alipore", "lat": 22.5332, "lng": 88.3314, "radius": 0.010},
            {"name": "Gariahat", "lat": 22.5195, "lng": 88.3653, "radius": 0.012},
            {"name": "Jadavpur", "lat": 22.4988, "lng": 88.3714, "radius": 0.012}
        ]
    },
    "Chennai": {
        "state": "Tamil Nadu",
        "base_inr": 2600,
        "count": 3000,
        "neighbourhoods": [
            {"name": "T. Nagar", "lat": 13.0418, "lng": 80.2341, "radius": 0.012},
            {"name": "Adyar", "lat": 13.0012, "lng": 80.2565, "radius": 0.010},
            {"name": "Besant Nagar", "lat": 12.9982, "lng": 80.2664, "radius": 0.007},
            {"name": "Mylapore", "lat": 13.0368, "lng": 80.2676, "radius": 0.009},
            {"name": "Nungambakkam", "lat": 13.0569, "lng": 80.2425, "radius": 0.012},
            {"name": "Velachery", "lat": 12.9759, "lng": 80.2212, "radius": 0.015},
            {"name": "Anna Nagar", "lat": 13.0850, "lng": 80.2101, "radius": 0.015},
            {"name": "Alwarpet", "lat": 13.0336, "lng": 80.2520, "radius": 0.010}
        ]
    }
}

ROOM_TYPES = [
    ("Entire home/apt", 0.55, 1.45),
    ("Private room", 0.35, 0.85),
    ("Hotel room", 0.07, 1.20),
    ("Shared room", 0.03, 0.45)
]

random.seed(42)
start_id = 10000001
os.makedirs("data/raw", exist_ok=True)
output_path = "data/raw/india_listings.csv"

fieldnames = [
    "id", "name", "neighbourhood_cleansed", "latitude", "longitude",
    "room_type", "property_type", "accommodates", "bedrooms", "beds",
    "price", "minimum_nights", "number_of_reviews", "review_scores_rating",
    "city", "state", "country", "currency"
]

total_generated = 0

with open(output_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    
    for city, config in NEIGHBOURHOOD_POLYGONS.items():
        base = config["base_inr"]
        count = config["count"]
        neigh_list = config["neighbourhoods"]
        
        for _ in range(count):
            start_id += 1
            # Pick room type
            r_val = random.random()
            cum = 0
            selected_room = "Entire home/apt"
            room_mult = 1.0
            for r_type, prob, mult in ROOM_TYPES:
                cum += prob
                if r_val <= cum:
                    selected_room = r_type
                    room_mult = mult
                    break
            
            neigh = random.choice(neigh_list)
            # Confine precisely within verified dry land radius
            rad = neigh["radius"]
            lat = neigh["lat"] + random.uniform(-rad, rad)
            lng = neigh["lng"] + random.uniform(-rad, rad)
            
            # Specific coastal water boundaries guard
            if city == "Mumbai":
                # Ensure it stays on land (East of Arabian sea coastline)
                if lat < 19.00 and lng < 72.812:
                    lng = 72.825 + random.uniform(0.002, 0.015)
                elif lat >= 19.00 and lng < 72.820:
                    lng = 72.830 + random.uniform(0.002, 0.015)
            elif city == "Goa":
                # Ensure it stays east of the Arabian Sea coastline
                if lng < 73.742:
                    lng = 73.748 + random.uniform(0.005, 0.02)
            elif city == "Chennai":
                # Ensure it stays west of Bay of Bengal (coastline is ~80.28)
                if lng > 80.278:
                    lng = 80.260 - random.uniform(0.005, 0.015)
            elif city == "Kolkata":
                # Ensure it stays away from middle of Hooghly River
                if 88.338 < lng < 88.345:
                    lng = 88.355 + random.uniform(0.005, 0.01)
                    
            accommodates = random.choices([1, 2, 3, 4, 6, 8], weights=[10, 45, 15, 20, 7, 3])[0]
            bedrooms = max(1, round(accommodates / 2.2))
            beds = max(1, round(accommodates / 1.5))
            
            base_usd = (base / 84.0)
            price_usd = (base_usd * room_mult * (1 + (accommodates * 0.18) + (bedrooms * 0.22))) * random.uniform(0.85, 1.25)
            price_usd = round(max(15.0, min(1800.0, price_usd)), 2)
            
            rating = round(random.betavariate(8, 1.2) * 2 + 3.0, 2)
            rating = min(5.0, max(3.5, rating))
            reviews = int(random.expovariate(1/35))
            min_nights = random.choice([1, 1, 2, 2, 3, 5])
            
            writer.writerow({
                "id": start_id,
                "name": f"{selected_room} in {neigh['name']}, {city}",
                "neighbourhood_cleansed": neigh["name"],
                "latitude": round(lat, 6),
                "longitude": round(lng, 6),
                "room_type": selected_room,
                "property_type": f"{selected_room} in building",
                "accommodates": accommodates,
                "bedrooms": bedrooms,
                "beds": beds,
                "price": f"${price_usd}",
                "minimum_nights": min_nights,
                "number_of_reviews": reviews,
                "review_scores_rating": rating,
                "city": city,
                "state": config["state"],
                "country": "India",
                "currency": "INR"
            })
            total_generated += 1

print(f"[SUCCESS] Land-anchored {total_generated:,} Indian Airbnb listings generated in {output_path}")
