import ast
import pandas as pd


class RatingExtractor:
    @staticmethod
    def extract_ratings(r) -> pd.Series:
        """Extracts normalized and raw ratings from various formats."""
        if pd.isna(r):
            return pd.Series({"normalized": None, "raw": None})

        # If it's a string that looks like a dict
        if isinstance(r, str):
            try:
                r = ast.literal_eval(r)
            except Exception:
                return pd.Series({"normalized": None, "raw": None})

        # If it's a dict
        if isinstance(r, dict):
            return pd.Series({"normalized": r.get("normalized"), "raw": r.get("raw")})

        # If it's a list (you can inspect manually before extracting)
        if isinstance(r, list):
            return pd.Series({"normalized": None, "raw": None})

        return pd.Series({"normalized": None, "raw": None})
