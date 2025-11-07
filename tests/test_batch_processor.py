# import pandas as pd

# from src.sentiment_aspect.batch_processor import BatchProcessor


# def test_split_into_batches_handles_remainder():
#     texts = [f"text-{i}" for i in range(5)]
#     df = pd.DataFrame({"text_for_analysis": texts})
#     processor = BatchProcessor(batch_size=2)

#     batches = processor.split_into_batches(df)

#     assert len(batches) == 3
#     assert batches[0] == ["text-0", "text-1"]
#     assert batches[1] == ["text-2", "text-3"]
#     assert batches[2] == ["text-4"]


# def test_process_batches_calls_extractor_for_each_batch():
#     df = pd.DataFrame({"text_for_analysis": [f"text-{i}" for i in range(4)]})
#     processor = BatchProcessor(batch_size=2)

#     class DummyExtractor:
#         def __init__(self):
#             self.calls = []

#         def extract_aspects(self, batch):
#             self.calls.append(list(batch))
#             return [{"batch": len(self.calls), "payload": batch}]

#     extractor = DummyExtractor()

#     results = processor.process_batches(extractor, df)

#     assert extractor.calls == [["text-0", "text-1"], ["text-2", "text-3"]]
#     assert results == [
#         {"batch": 1, "payload": ["text-0", "text-1"]},
#         {"batch": 2, "payload": ["text-2", "text-3"]},
#     ]
