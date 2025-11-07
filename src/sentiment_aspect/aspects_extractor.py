import time


# Function to extract aspects and sentiment from the text
def extract_aspects_from_text(extractor, text):
    try:
        start_time = time.time()
        # Extract aspects and sentiment using the model
        results = extractor.predict(
            [text],
            print_result=False,
            save_result=False,
            ignore_error=True,
            pred_sentiment=True,
        )

        processing_time_ms = int((time.time() - start_time) * 1000)

        if not results or len(results) == 0:
            print(f"No results found for text: {text}")
            return []

        # Extract the first result (since we only sent one text)
        pyabsa_result = results[0]

        # Extract aspects, sentiments, and confidences
        aspects = []
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

            aspects.append(
                {
                    "aspect": aspect,
                    "evidence_span": evidence_span,
                    "polarity": sentiment,
                    "confidence": confidence,
                }
            )

        return {
            "aspects": aspects,
            "meta": {"model": "pyabsa-multilingual", "latency_ms": processing_time_ms},
        }

    except Exception as e:
        print(f"Error during sentiment extraction: {e}")
        return []
