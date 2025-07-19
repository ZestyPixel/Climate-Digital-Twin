import requests
import pandas as pd
import time

# Coordinates of key cities along the Ganga
cities = {
    "Rishikesh": (30.0869, 78.2676),
    "Kanpur": (26.4499, 80.3319),
    "Varanasi": (25.3176, 82.9739),
    "Patna": (25.5941, 85.1376),
    "Bhagalpur": (25.2532, 87.0000),
    "Farakka": (24.7992, 87.9220),
    "Kolkata": (22.5726, 88.3639)
}

all_data = []

for city, (lat, lon) in cities.items():
    print(f"\n📡 Fetching for {city} ({lat}, {lon})")

    # Correct date format: YYYYMM
    url = (
        f"https://power.larc.nasa.gov/api/temporal/monthly/point"
        f"?parameters=T2M,PRECTOTCORR&community=AG"
        f"&longitude={lon}&latitude={lat}"
        f"&start=20000101&end=20231231&format=JSON"
    )

    response = requests.get(url)
    print("Status Code:", response.status_code)
    print("URL:", response.url)

    if response.status_code != 200:
        print(f"❌ Failed to fetch data for {city}")
        continue

    json_data = response.json()

    try:
        data = json_data["parameters"]
        print("✔️ Data keys from NASA:", list(data.keys()))
    except KeyError:
        print("❌ 'parameters' not found in response JSON.")
        print("Response JSON:", json_data)
        continue

    temps = data.get("T2M", {})
    rain = data.get("PRECTOTCORR", {})

    print(f"🌡️ T2M data points: {len(temps)}, 🌧️ Rain data points: {len(rain)}")

    for date in temps:
        if date in rain and date.isdigit():
            year = int(date[:4])
            month = int(date[4:])

            temp_val = temps[date]
            rain_val = rain[date] * 30  # convert mm/day → mm/month

            all_data.append({
                "City": city,
                "Latitude": lat,
                "Longitude": lon,
                "Year": year,
                "Month": month,
                "Rainfall_mm": round(rain_val, 2),
                "Temperature_C": round(temp_val, 2),
                "Source": "NASA_POWER"
            })

    print(f"✅ Added {len(all_data)} total rows so far...")
    time.sleep(1)  # NASA API rate limit safety

# Save to CSV if data exists
if all_data:
    df = pd.DataFrame(all_data)
    print(f"\n📄 Final total rows: {len(df)}")
    df.to_csv("../data/ganga_nasa_2000_2023.csv", index=False)
    print("✅ Saved to ../data/ganga_nasa_2000_2023.csv")
else:
    print("⚠️ No data collected — check API response formatting.")
