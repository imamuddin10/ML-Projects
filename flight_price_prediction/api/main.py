from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from schema import FlightInput, PredictionOutput
from model import predict_price

# ── App Setup ────────────────────────────────────────────
app = FastAPI(
    title       = "✈️ Flight Price Predictor API",
    description = "Predicts flight prices using ML. Built for Fareportal use case.",
    version     = "1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# ── Routes ───────────────────────────────────────────────
@app.get("/")
def root():
    return {
        "message": "✈️ Flight Price Predictor API is live!",
        "docs"   : "/docs",
        "health" : "/health"
    }

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict", response_model=PredictionOutput)
def predict(flight: FlightInput):
    try:
        result = predict_price(flight.dict())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))