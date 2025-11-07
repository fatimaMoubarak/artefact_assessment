# dataframe_processor.py
import pandas as pd
from rating_extractor import RatingExtractor
from tag_parser import TagParser
from duplicates_checks import print_duplicate_offer_destination


class DataFrameProcessor:
    def __init__(self, df: pd.DataFrame, mapping: dict):
        """Initializes the DataFrameProcessor with a DataFrame and a mapping dictionary."""
        self.df = df
        self.mapping = mapping

    def process_ratings(self):
        """Extracts and normalizes ratings from the DataFrame."""
        self.df[["normalized", "raw"]] = self.df["ratings"].apply(
            RatingExtractor.extract_ratings
        )

    def process_tags(self):
        """Flattens tags in the DataFrame based on the provided mapping."""
        self.df = TagParser.flatten_tags(self.df, self.mapping)

    def find_duplicates(self):
        """Prints duplicate offer destinations in the DataFrame."""
        print_duplicate_offer_destination(self.df)
