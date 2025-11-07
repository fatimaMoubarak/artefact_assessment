import ast
import pandas as pd


class TagParser:
    @staticmethod
    def _parse_tags_cell(cell):
        """Return a list of tag codes for this cell."""
        if pd.isna(cell):
            return []
        # If the cell is a string that looks like a list, parse it
        if isinstance(cell, str):
            try:
                parsed = ast.literal_eval(cell)
            except Exception:
                # Not parseable -> treat as single code string
                return [cell]
        else:
            parsed = cell

        # parsed may be list of dicts like {'value': 'code', 'sentiment': ...}
        codes = []
        if isinstance(parsed, list):
            for item in parsed:
                if isinstance(item, dict) and "value" in item:
                    codes.append(item["value"])
                elif isinstance(item, str):
                    codes.append(item)
        return codes

    @staticmethod
    def flatten_tags(
        df: pd.DataFrame,
        mapping: dict,
        tags_col: str = "tags",
        drop_original: bool = False,
    ) -> pd.DataFrame:
        """
        Flatten a tags column into offer/destination pairs using a mapping dict.
        """
        tag_map = mapping.get("tags_mapping", {})

        # For each row, build a list of (offer, destination) pairs (destination may be None)
        pairs_per_row = []
        max_pairs = 0
        for cell in df[tags_col].tolist():
            codes = TagParser._parse_tags_cell(cell)
            pairs = []
            for code in codes:
                vals = tag_map.get(code, [])
                # Normalize to list
                if not isinstance(vals, list):
                    vals = [vals]
                offer = vals[0] if len(vals) >= 1 else None
                destination = vals[1] if len(vals) >= 2 else None
                pairs.append((offer, destination))
            pairs_per_row.append(pairs)
            if len(pairs) > max_pairs:
                max_pairs = len(pairs)

        # Create columns: offer/destination for the first pair,
        # then offer_2/destination_2 ... up to max_pairs
        out_cols = []
        if max_pairs >= 1:
            out_cols.extend(["offer", "destination"])
        for i in range(2, max_pairs + 1):
            out_cols.extend([f"offer_{i}", f"destination_{i}"])

        # Initialize with NaNs
        for col in out_cols:
            df[col] = pd.NA

        # Fill row-by-row
        for idx, pairs in enumerate(pairs_per_row):
            for j, (offer, dest) in enumerate(pairs, start=1):
                if j == 1:
                    df.at[idx, "offer"] = offer
                    df.at[idx, "destination"] = dest
                else:
                    df.at[idx, f"offer_{j}"] = offer
                    df.at[idx, f"destination_{j}"] = dest

        if drop_original:
            df = df.drop(columns=[tags_col])

        return df
