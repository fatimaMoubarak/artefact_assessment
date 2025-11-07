from pyabsa import AspectTermExtraction as ATEPC


class ModelLoader:
    def __init__(self, model_name="multilingual", auto_device=True):
        self.model_name = model_name
        self.auto_device = auto_device
        self.extractor = None

    def load_model(self):
        try:
            print("Loading PyABSA multilingual model...")
            self.extractor = ATEPC.AspectExtractor(
                self.model_name, auto_device=self.auto_device
            )
            print("PyABSA model loaded successfully.")
        except Exception as e:
            print(f"Failed to load PyABSA model: {e}")
            self.extractor = None
        return self.extractor
