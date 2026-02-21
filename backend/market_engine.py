import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
prices_file = os.path.join(BASE_DIR, "../data/prices.csv")

try:
    prices_df = pd.read_csv(prices_file)
except Exception as e:
    print("Error loading prices.csv:", e)
    prices_df = pd.DataFrame(columns=["crop", "market", "price"])

def get_price_forecast(crop, location=None):
    try:
        df = prices_df[prices_df["crop"].str.lower() == crop.lower()]
        if location:
            df = df[df["market"].str.lower() == location.lower()]

        if df.empty:
            return f"No market data available for {crop} in {location}."

        price = int(df.iloc[0]["price"])
        return {
            "today_price": price,
            "future_price": price,
            "trend": "stable",
            "recommendation": "Check market rates"
        }

    except Exception as e:
        print("Price fetch error:", e)
        return f"No market data available for {crop} in {location}."