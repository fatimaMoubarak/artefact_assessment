from fastapi.testclient import TestClient

import app


def test_predict_endpoint_success(monkeypatch):
    sample_response = [
        {
            "text_id": 0,
            "aspect": "staff",
            "evidence_span": "staff was lovely",
            "polarity": "Positive",
            "confidence": 0.95,
            "model": "pyabsa-multilingual",
            "latency_ms": 120,
        }
    ]

    def fake_predictor(df):
        assert list(df.columns) == ["text_for_analysis"]
        assert df.iloc[0]["text_for_analysis"] == "Great staff"
        return sample_response

    monkeypatch.setattr(app, "predictor", fake_predictor)
    client = TestClient(app.app)

    response = client.post(
        "/predict", json=[{"text_for_analysis": "Great staff"}]
    )

    assert response.status_code == 200
    assert response.json() == sample_response


def test_predict_endpoint_handles_empty_predictions(monkeypatch):
    monkeypatch.setattr(app, "predictor", lambda df: [])
    client = TestClient(app.app)

    response = client.post(
        "/predict", json=[{"text_for_analysis": "No aspects"}]
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "No predictions could be made."
