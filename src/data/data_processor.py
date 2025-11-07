# dataframe_processor.py
import pandas as pd
from rating_extractor import RatingExtractor
from tag_parser import TagParser
from duplicates_checks import print_duplicate_offer_destination


class DataFrameProcessor:
    def __init__(self, df: pd.DataFrame, mapping: dict):
        self.df = df
        self.mapping = mapping

    def process_ratings(self):
        self.df[["normalized", "raw"]] = self.df["ratings"].apply(
            RatingExtractor.extract_ratings
        )

    def process_tags(self):
        self.df = TagParser.flatten_tags(self.df, self.mapping)

    def find_duplicates(self):
        print_duplicate_offer_destination(self.df)
