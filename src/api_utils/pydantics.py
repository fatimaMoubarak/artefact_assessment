from pydantic import BaseModel


# Pydantic model for incoming request data
class TextData(BaseModel):
    text_for_analysis: str


class PredictionResponse(BaseModel):
    text_id: int
    aspect: str
    evidence_span: str
    polarity: str
    confidence: float
    model: str
    latency_ms: int
