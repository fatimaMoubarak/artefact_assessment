class BatchProcessor:
    def __init__(self, batch_size=100):
        self.batch_size = batch_size

    def split_into_batches(self, data):
        return [
            data.iloc[i: i + self.batch_size]["text_for_analysis"].tolist()
            for i in range(0, len(data), self.batch_size)
        ]

    def process_batches(self, extractor, data):
        batch_results = []
        batches = self.split_into_batches(data)
        for batch in batches:
            result = extractor.extract_aspects(batch)
            batch_results.extend(result)
        return batch_results
