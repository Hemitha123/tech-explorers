import pandas as pd
import os

# -----------------------------
# Function to fetch weather from CSV
# -----------------------------
def get_weather(location, season):
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        weather_csv = os.path.join(base_dir, "../data/weather_data.csv")
        weather_df = pd.read_csv(weather_csv)

        row = weather_df[
            (weather_df["location"].str.lower() == location.lower()) &
            (weather_df["season"].str.lower() == season.lower())
        ]

        if not row.empty:
            temp = float(row.iloc[0]["temp"])
            rainfall = float(row.iloc[0]["rainfall"])
            humidity = float(row.iloc[0]["humidity"])
            return temp, rainfall, humidity
        else:
            return 25.0, 0.0, 60.0  # default
    except Exception as e:
        print("Weather fetch error:", e)
        return 25.0, 0.0, 60.0

# -----------------------------
# Function to recommend crop
# -----------------------------
def recommend_crop(soil, water, season=None):
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        crops_csv = os.path.join(base_dir, "../data/crops.csv")
        crops = pd.read_csv(crops_csv)
    except Exception as e:
        print("Crops CSV read error:", e)
        return "NoCrop", 0, 0, 0

    score_list = []

    for _, row in crops.iterrows():
        score = 0

        # Soil match
        if row["soil"].lower() == soil.lower():
            score += 50
        else:
            score += 10

        # Water match
        if row["water_need"].lower() == water.lower():
            score += 30
        elif row["water_need"].lower() == "low" and water.lower() == "medium":
            score += 15

        # Season match
        if season and row.get("season", "").lower() == season.lower():
            score += 20

        # Yield contribution
        score += row["base_yield"]

        score_list.append((row["crop"], score, row["price"], row["base_yield"]))

    if score_list:
        best = sorted(score_list, key=lambda x: x[1], reverse=True)[0]
        return best
    else:
        return "NoCrop", 0, 0, 0

# -----------------------------
# Main function to combine crop + weather
# -----------------------------
def get_crop_plan(location, soil, water, season=None):
    temperature, rainfall, humidity = get_weather(location, season)
    crop, score, price, base_yield = recommend_crop(soil, water, season)

    return {
        "crop": crop,
        "score": score,
        "price": price,
        "base_yield": base_yield,
        "temperature": temperature,
        "rainfall": rainfall,
        "humidity": humidity
    }