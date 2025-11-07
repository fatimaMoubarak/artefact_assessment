def test_predict_endpoint_success(monkeypatch):
    from fastapi.testclient import TestClient
    from types import SimpleNamespace
    import app

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

    class FakeIloc:
        def __init__(self, rows):
            self._rows = rows

        def __getitem__(self, index):
            return self._rows[index]

    class FakeDataFrame:
        def __init__(self, rows):
            self.records = rows
            self.columns = list(rows[0].keys()) if rows else []
            self.iloc = FakeIloc(rows)

    def fake_dataframe(rows):
        assert rows == [{"text_for_analysis": "Great staff"}]
        return FakeDataFrame(rows)

    def fake_predictor(df):
        assert isinstance(df, FakeDataFrame)
        assert df.records[0]["text_for_analysis"] == "Great staff"
        return sample_response

    monkeypatch.setattr(app, "pd", SimpleNamespace(DataFrame=fake_dataframe))
    monkeypatch.setattr(app, "predictor", fake_predictor)
    client = TestClient(app.app)

    response = client.post(
        "/predict", json=[{"text_for_analysis": "Great staff"}]
    )

    assert response.status_code == 200
    assert response.json() == sample_response


def test_predict_endpoint_handles_empty_predictions(monkeypatch):
    from fastapi.testclient import TestClient
    from types import SimpleNamespace
    import app

    class FakeIloc:
        def __init__(self, rows):
            self._rows = rows

        def __getitem__(self, index):
            return self._rows[index]

    class FakeDataFrame:
        def __init__(self, rows):
            self.records = rows
            self.iloc = FakeIloc(rows)

    monkeypatch.setattr(
        app,
        "pd",
        SimpleNamespace(DataFrame=lambda rows: FakeDataFrame(rows)),
    )
    monkeypatch.setattr(app, "predictor", lambda df: [])
    client = TestClient(app.app)

    response = client.post(
        "/predict", json=[{"text_for_analysis": "No aspects"}]
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "No predictions could be made."
