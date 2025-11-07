from fastapi import FastAPI, HTTPException
import pandas as pd
from typing import List
from src.sentiment_aspect.main import predictor
from src.api_utils.pydantics import TextData, PredictionResponse

# Create FastAPI app
app = FastAPI()


@app.post("/predict", response_model=List[PredictionResponse])
async def predict(data: List[TextData]):
    try:
        # Convert input data to a pandas DataFrame
        df = pd.DataFrame([item.model_dump() for item in data])

        # Get prediction results using the predictor function
        results = predictor(df)

        if not results:
            raise HTTPException(status_code=400, detail="No predictions could be made.")

        return results

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred: {str(e)}")
