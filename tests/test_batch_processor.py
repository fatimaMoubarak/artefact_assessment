class _FakeSeries:
    def __init__(self, data):
        self._data = list(data)

    def tolist(self):
        return list(self._data)


class _FakeSlice:
    def __init__(self, data):
        self._data = list(data)

    def __getitem__(self, key):
        if key != "text_for_analysis":
            raise KeyError(key)
        return _FakeSeries(self._data)


class _FakeIloc:
    def __init__(self, parent):
        self._parent = parent

    def __getitem__(self, slice_obj):
        return _FakeSlice(self._parent._data[slice_obj])


class _FakeDataFrame:
    def __init__(self, texts):
        self._data = list(texts)
        self.iloc = _FakeIloc(self)

    def __len__(self):
        return len(self._data)


def test_split_into_batches_handles_remainder():
    from src.sentiment_aspect.batch_processor import BatchProcessor

    df = _FakeDataFrame([f"text-{i}" for i in range(5)])
    processor = BatchProcessor(batch_size=2)

    batches = processor.split_into_batches(df)

    assert len(batches) == 3
    assert batches[0] == ["text-0", "text-1"]
    assert batches[1] == ["text-2", "text-3"]
    assert batches[2] == ["text-4"]


def test_process_batches_calls_extractor_for_each_batch():
    from src.sentiment_aspect.batch_processor import BatchProcessor

    df = _FakeDataFrame([f"text-{i}" for i in range(4)])
    processor = BatchProcessor(batch_size=2)

    class DummyExtractor:
        def __init__(self):
            self.calls = []

        def extract_aspects(self, batch):
            self.calls.append(list(batch))
            return [{"batch": len(self.calls), "payload": batch}]

    extractor = DummyExtractor()

    results = processor.process_batches(extractor, df)

    assert extractor.calls == [["text-0", "text-1"], ["text-2", "text-3"]]
    assert results == [
        {"batch": 1, "payload": ["text-0", "text-1"]},
        {"batch": 2, "payload": ["text-2", "text-3"]},
    ]
