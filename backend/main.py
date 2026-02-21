from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import random

app = FastAPI(title="AgroFusion AI")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/test")
def test():
    return {"message": "Hello from backend"}

# -----------------------------
# Input schema
# -----------------------------
class FarmInput(BaseModel):
    location: str
    land_size: float
    soil_type: str
    water_availability: str
    previous_crop: str | None = None
    budget: str | None = None
    season: str
    temperature: float | None = None
    rainfall: float | None = None
    humidity: float | None = None

# -----------------------------
# Crop database (expandable)
# -----------------------------
crops_db = [
    {
        "name": "Rice",
        "soil": ["loam", "clay"],
        "season": ["Kharif"],
        "water_need": "high",
        "base_yield": 35,
        "price": 1500
    },
    {
        "name": "Maize",
        "soil": ["loam", "red"],
        "season": ["Kharif", "Rabi"],
        "water_need": "medium",
        "base_yield": 22,
        "price": 1800
    },
    {
        "name": "Groundnut",
        "soil": ["red", "sandy"],
        "season": ["Rabi"],
        "water_need": "low",
        "base_yield": 18,
        "price": 2000
    }
]

# -----------------------------
# SMART crop scoring
# -----------------------------
def score_crop(crop, data: FarmInput):
    score = 0

    # soil match
    if data.soil_type.lower() in crop["soil"]:
        score += 0.4

    # season match
    if data.season in crop["season"]:
        score += 0.3

    # water match
    if data.water_availability == crop["water_need"]:
        score += 0.3

    return score

def select_best_crop(data: FarmInput):
    best_crop = None
    best_score = -1

    for crop in crops_db:
        s = score_crop(crop, data)
        if s > best_score:
            best_score = s
            best_crop = crop

    return best_crop, round(best_score, 2)

# -----------------------------
# Dynamic yield calculation
# -----------------------------
def calculate_yield(base_yield, land_size, rain, water):
    multiplier = 1.0

    if rain:
        if rain < 80:
            multiplier -= 0.2
        elif rain > 400:
            multiplier += 0.1

    if water == "high":
        multiplier += 0.1
    elif water == "low":
        multiplier -= 0.15

    return round(base_yield * land_size * multiplier, 2)

# -----------------------------
# Weather risk
# -----------------------------
def calculate_weather_risk(temp, rain):
    if temp and temp > 36:
        return "High Risk"
    if rain and rain < 60:
        return "Medium Risk"
    return "Low Risk"

# -----------------------------
# Prevention alerts
# -----------------------------
def generate_alerts(crop_name, humidity, rain):
    alerts = []

    if crop_name == "Rice" and humidity and humidity > 75:
        alerts.append({
            "type": "Fungal Risk",
            "message": "High chance of fungal infection in Rice",
            "action": "Spray neem oil or recommended fungicide"
        })

    if crop_name == "Groundnut" and rain and rain > 500:
        alerts.append({
            "type": "Rot Risk",
            "message": "Excess moisture may cause pod rot",
            "action": "Improve field drainage"
        })

    return alerts

# -----------------------------
# Market forecast (controlled)
# -----------------------------
def market_forecast(today_price):
    change_pct = random.uniform(-0.08, 0.12)
    future_price = round(today_price * (1 + change_pct), 2)

    if future_price > today_price:
        trend = "rising"
        rec = "Hold for better price"
    elif future_price < today_price:
        trend = "falling"
        rec = "Consider selling soon"
    else:
        trend = "stable"
        rec = "Market stable"

    return {
        "today_price": round(today_price / 75, 2),
        "future_price": round(future_price / 75, 2),
        "trend": trend,
        "recommendation": rec
    }

# -----------------------------
# MAIN ENDPOINT
# -----------------------------
@app.post("/plan")
def generate_plan(data: FarmInput):
    try:
        # ✅ smart crop selection
        crop, confidence = select_best_crop(data)

        # ✅ dynamic yield
        expected_yield = calculate_yield(
            crop["base_yield"],
            data.land_size,
            data.rainfall,
            data.water_availability
        )

        # ✅ weather
        risk = calculate_weather_risk(data.temperature, data.rainfall)

        weather_summary = {
            "avg_temp": data.temperature or 28,
            "total_rain": data.rainfall or 120
        }

        # ✅ alerts
        alerts = generate_alerts(
            crop["name"],
            data.humidity,
            data.rainfall
        )

        # ✅ market
        market = market_forecast(crop["price"])

        return {
            "recommended_crop": crop["name"],
            "expected_yield": f"{expected_yield} quintal",
            "estimated_price_per_quintal": f"₹{crop['price']}",
            "confidence_score": confidence,
            "weather_risk": risk,
            "weather_summary": weather_summary,
            "prevention_alerts": alerts,
            "market_advice": market,
            "advice": f"Based on your soil and water conditions, {crop['name']} is recommended for your farm."
        }

    except Exception as e:
        return {"error": str(e)}






# # backend/main.py

# from fastapi import FastAPI
# from pydantic import BaseModel
# import random

# app = FastAPI(title="AgroFusion AI Demo Compact Output")

# # -----------------------------
# # Input schema
# # -----------------------------
# class FarmInput(BaseModel):
#     location: str
#     land_size: float
#     soil_type: str
#     water_availability: str
#     previous_crop: str = None
#     budget: str = None
#     season: str
#     temperature: float = None
#     rainfall: float = None
#     humidity: float = None

# # -----------------------------
# # Demo crop data
# # -----------------------------
# demo_crops = [
#     {"name": "Rice", "soil_type": "loam", "season": "Kharif", "base_yield": 35, "price": 1500},
#     {"name": "Maize", "soil_type": "red", "season": "Kharif", "base_yield": 22, "price": 1800},
#     {"name": "Groundnut", "soil_type": "red", "season": "Rabi", "base_yield": 25, "price": 2000},
#     {"name": "Wheat", "soil_type": "loam", "season": "Rabi", "base_yield": 30, "price": 1700},
# ]

# # -----------------------------
# # Helper functions
# # -----------------------------
# def get_crop_plan(location, soil, water, season):
#     # Demo: select first matching crop
#     for crop in demo_crops:
#         if crop["soil_type"] == soil and crop["season"] == season:
#             score = random.uniform(0.7, 0.95)
#             return {
#                 "crop": crop["name"],
#                 "score": round(score, 2),
#                 "price": crop["price"],
#                 "base_yield": crop["base_yield"],
#             }
#     # fallback crop
#     fallback = demo_crops[0]
#     return {
#         "crop": fallback["name"],
#         "score": 0.8,
#         "price": fallback["price"],
#         "base_yield": fallback["base_yield"],
#     }

# def calculate_future_price(today_price, fluctuation_percent=10):
#     min_price = today_price * (1 - fluctuation_percent / 100)
#     max_price = today_price * (1 + fluctuation_percent / 100)
#     return round(random.uniform(min_price, max_price), 2)

# def calculate_risk(temperature, rainfall, humidity):
#     # simple demo logic
#     if temperature is None or rainfall is None or humidity is None:
#         return "Unknown"
#     if temperature > 35 or temperature < 15:
#         return "High Risk"
#     if rainfall < 100:
#         return "Medium Risk"
#     return "Low Risk"

# # -----------------------------
# # Main endpoint
# # -----------------------------
# @app.post("/plan")
# def generate_plan(data: FarmInput):
#     try:
#         # Crop recommendation
#         crop_plan = get_crop_plan(
#             location=data.location,
#             soil=data.soil_type,
#             water=data.water_availability,
#             season=data.season
#         )

#         crop = crop_plan["crop"]
#         score = crop_plan["score"]
#         today_price = float(crop_plan["price"])
#         base_yield = crop_plan["base_yield"]

#         # Yield
#         total_yield = base_yield * data.land_size

#         # Future price
#         future_price = calculate_future_price(today_price, fluctuation_percent=10)

#         # Weather risk
#         risk = calculate_risk(data.temperature, data.rainfall, data.humidity)

#         # Return compact JSON
#         return {
#             "recommended_crop": crop,
#             "expected_yield": f"{round(total_yield, 2)} quintal",
#             "today_price": f"₹{today_price}",
#             "future_price": f"₹{future_price}",
#             "confidence_score": round(score, 2),
#             "weather_risk": risk
#         }

#     except Exception as e:
#         print("Error in /plan:", e)
#         return {"error": str(e)}