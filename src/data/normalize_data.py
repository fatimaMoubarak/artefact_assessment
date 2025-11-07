import ast
import pandas as pd


def extract_ratings(r):
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


def flatten_tags(
    df: pd.DataFrame,
    mapping: dict,
    tags_col: str = "tags",
    drop_original: bool = False,
) -> pd.DataFrame:
    """
    Flatten a tags column into offer/destination pairs using a mapping dict.

    Rules:
      - For each tag code, the mapping value is a list: [offer, destination]
      - If only one element exists -> treat it as offer (destination = NaN)
      - If a row has multiple tags -> create offer_2/destination_2, offer_3/destination_3, etc.
      - First pair uses columns 'offer' and 'destination' (no suffix); subsequent pairs are suffixed.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing the tags column.
    mapping : dict
        Dict with key 'tags_mapping' mapping code -> [offer, destination].
    tags_col : str, default 'tags'
        Name of the column that holds the list (or stringified list) of tag dicts or codes.
    drop_original : bool, default False
        If True, drops the original tags column.

    Returns
    -------
    pd.DataFrame
        The original df with added flattened columns.
    """
    tag_map = mapping.get("tags_mapping", {})

    # For each row, build a list of (offer, destination) pairs (destination may be None)
    pairs_per_row = []
    max_pairs = 0
    for cell in df[tags_col].tolist():
        codes = _parse_tags_cell(cell)
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


def print_duplicate_offer_destination(df):
    """Print rows where duplicate offer-destination pairs are found."""
    for idx, row in df.iterrows():
        # Collect all (offer, destination) pairs from the row
        pairs = []
        for i in range(1, 6):  # Loop through offer_2 to offer_5
            offer = row[f"offer_{i}"] if f"offer_{i}" in row else row["offer"]
            destination = (
                row[f"destination_{i}"]
                if f"destination_{i}" in row
                else row["destination"]
            )
            if pd.notna(offer) and pd.notna(destination):
                pairs.append((offer, destination))

        # Check for duplicates in pairs
        if len(pairs) != len(set(pairs)):  # If duplicates exist
            print(f"Row {idx} has duplicate offer-destination pairs: {pairs}")
            print(
                row[
                    [
                        "id",
                        "tags",
                        "offer",
                        "destination",
                        "offer_2",
                        "destination_2",
                        "offer_3",
                        "destination_3",
                        "offer_4",
                        "destination_4",
                        "offer_5",
                        "destination_5",
                    ]
                ]
            )
