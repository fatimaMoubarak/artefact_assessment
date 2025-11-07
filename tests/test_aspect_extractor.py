def test_extract_aspects_flattens_model_output(monkeypatch):
    from src.sentiment_aspect.aspect_extractor import AspectExtractor

    fake_results = [
        {
            "aspect": ["service", "room"],
            "sentiment": ["Positive", "Negative"],
            "confidence": [0.9, 0.2],
            "tokens": ["The", "service", "was", "great", "room", "was", "tiny"],
            "position": [[1, 2, 3], [4, 5, 6]],
        }
    ]

    # Force a deterministic latency calculation.
    time_values = iter([100.0, 100.25])

    def fake_time():
        return next(time_values)

    monkeypatch.setattr(
        "src.sentiment_aspect.aspect_extractor.time.time", fake_time
    )

    class DummyModel:
        def predict(self, *args, **kwargs):
            return fake_results

    extractor = AspectExtractor(extractor=DummyModel())

    rows = extractor.extract_aspects(["dummy text"])

    assert rows == [
        {
            "text_id": 0,
            "aspect": "service",
            "evidence_span": "service was great",
            "polarity": "Positive",
            "confidence": 0.9,
            "model": "pyabsa-multilingual",
            "latency_ms": 250,
        },
        {
            "text_id": 0,
            "aspect": "room",
            "evidence_span": "room was tiny",
            "polarity": "Negative",
            "confidence": 0.2,
            "model": "pyabsa-multilingual",
            "latency_ms": 250,
        },
    ]


def test_extract_aspects_handles_empty_results():
    from src.sentiment_aspect.aspect_extractor import AspectExtractor

    class DummyModel:
        def predict(self, *args, **kwargs):
            return []

    extractor = AspectExtractor(extractor=DummyModel())

    rows = extractor.extract_aspects(["no aspects here"])

    assert rows == []
