
from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException

from app.schemas import ListingInput, PredictionOutput


BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "model.joblib"

app = FastAPI(
    title="Airbnb Price Prediction API",
    description="Predicts nightly Airbnb listing prices in New York City.",
    version="1.0.0",
)

# Load the trained pipeline once when the application starts.
model = joblib.load(MODEL_PATH)


@app.get("/")
def home():
    return {
        "message": "Airbnb Price Prediction API",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "model_loaded": model is not None,
    }


@app.post("/predict", response_model=PredictionOutput)
def predict_price(listing: ListingInput):
    try:
        # Convert validated input into a one-row DataFrame.
        input_data = pd.DataFrame(
            [listing.model_dump()]
        )

        # The saved pipeline performs preprocessing and prediction.
        prediction = float(model.predict(input_data)[0])

        return PredictionOutput(
            predicted_price=round(max(0.0, prediction), 2)
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Prediction failed. Check the API logs.",
        ) from exc
