from model_loader import ModelLoader
from aspect_extractor import AspectExtractor
from batch_processor import BatchProcessor


def predictor(data):
    # Initialize Model Loader and Aspect Extractor
    model_loader = ModelLoader()
    extractor = model_loader.load_model()

    if extractor:
        aspect_extractor = AspectExtractor(extractor)
        batch_processor = BatchProcessor(batch_size=100)

        # Process the batches and get the results
        all_results = batch_processor.process_batches(aspect_extractor, data)
        return all_results
    else:
        print("Model loading failed. Cannot proceed.")
        return []
