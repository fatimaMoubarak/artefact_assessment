import pandas as pd


@staticmethod
def print_duplicate_offer_destination(df: pd.DataFrame) -> None:
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
