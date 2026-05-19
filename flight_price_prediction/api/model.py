import joblib
import numpy as np
import pandas as pd

# Load model once at startup
model = joblib.load('../src/flight_price_model_tuned.pkl')

AIRLINES = ['Air_India', 'GO_FIRST', 'Indigo', 'SpiceJet', 'Vistara']
CITIES   = ['Chennai', 'Delhi', 'Hyderabad', 'Kolkata', 'Mumbai']
TIMES    = ['Early_Morning', 'Evening', 'Late_Night', 'Morning', 'Night']


def preprocess(input_data: dict) -> pd.DataFrame:
    """Transform raw input into model-ready feature vector."""

    row = {}

    # ── EXACT ORDER as training data ─────────────────────
    row['stops']    = {'zero': 0, 'one': 1, 'two_or_more': 2}[input_data['stops']]
    row['class']    = 1 if input_data['travel_class'] == 'Business' else 0
    row['duration'] = input_data['duration']
    row['days_left']= input_data['days_left']

    # ── One-hot: airline ─────────────────────────────────
    for airline in AIRLINES:
        row[f'airline_{airline}'] = 1 if input_data['airline'] == airline else 0

    # ── One-hot: source_city ─────────────────────────────
    for city in CITIES:
        row[f'source_city_{city}'] = 1 if input_data['source_city'] == city else 0

    # ── One-hot: destination_city ────────────────────────
    for city in CITIES:
        row[f'destination_city_{city}'] = 1 if input_data['destination_city'] == city else 0

    # ── One-hot: departure_time ──────────────────────────
    for time in TIMES:
        row[f'departure_time_{time}'] = 1 if input_data['departure_time'] == time else 0

    # ── One-hot: arrival_time ────────────────────────────
    for time in TIMES:
        row[f'arrival_time_{time}'] = 1 if input_data['arrival_time'] == time else 0

    return pd.DataFrame([row])


def predict_price(input_data: dict) -> dict:
    """Run prediction and return price + advice."""

    features  = preprocess(input_data)
    log_price = model.predict(features)[0]
    price     = np.expm1(log_price)

    # Price range ±10%
    low  = round(price * 0.90, 0)
    high = round(price * 1.10, 0)

    # Booking advice based on days_left
    days = input_data['days_left']
    if days <= 7:
        advice = "⚠️ Book immediately — prices spike within 7 days!"
    elif days <= 21:
        advice = "📈 Prices rising soon — book in the next few days."
    elif days <= 45:
        advice = "✅ Good time to book — prices are stable."
    else:
        advice = "⏳ You can wait — prices may drop closer to 30 days."

    return {
        "predicted_price": round(price, 2),
        "price_range"    : f"₹{low:,.0f} – ₹{high:,.0f}",
        "advice"         : advice
    }