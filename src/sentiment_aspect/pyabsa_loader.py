from pyabsa import AspectTermExtraction as ATEPC


# Load the PyABSA multilingual model
def load_pyabsa_model():
    try:
        print("Loading PyABSA multilingual model...")
        extractor = ATEPC.AspectExtractor("multilingual", auto_device=True)
        print("PyABSA model loaded successfully.")
        return extractor
    except Exception as e:
        print(f"Failed to load PyABSA model: {e}")
        return None
