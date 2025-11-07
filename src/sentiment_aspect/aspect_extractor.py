import time


class AspectExtractor:
    def __init__(self, extractor):
        self.extractor = extractor

    def extract_aspects(self, texts):
        try:
            start_time = time.time()
            results = self.extractor.predict(
                texts,
                print_result=False,
                save_result=False,
                ignore_error=True,
                pred_sentiment=True,
            )
            processing_time_ms = int((time.time() - start_time) * 1000)

            if not results or len(results) == 0:
                print(f"No results found for texts: {texts}")
                return []

            flattened_results = []
            for text_idx, pyabsa_result in enumerate(results):
                for i, aspect in enumerate(pyabsa_result["aspect"]):
                    sentiment = (
                        pyabsa_result["sentiment"][i]
                        if i < len(pyabsa_result["sentiment"])
                        else "Neutral"
                    )
                    confidence = (
                        pyabsa_result["confidence"][i]
                        if i < len(pyabsa_result["confidence"])
                        else 0.0
                    )
                    evidence_span = (
                        " ".join(
                            [
                                pyabsa_result["tokens"][idx]
                                for idx in pyabsa_result["position"][i]
                            ]
                        )
                        if pyabsa_result["position"]
                        else aspect
                    )

                    flattened_results.append(
                        {
                            "text_id": text_idx,
                            "aspect": aspect,
                            "evidence_span": evidence_span,
                            "polarity": sentiment,
                            "confidence": confidence,
                            "model": "pyabsa-multilingual",
                            "latency_ms": processing_time_ms,
                        }
                    )

            return flattened_results

        except Exception as e:
            print(f"Error during sentiment extraction: {e}")
            return []
