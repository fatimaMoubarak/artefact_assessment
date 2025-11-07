# Imports
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import re

# Configure settings
warnings.filterwarnings("ignore")

plt.style.use("seaborn-v0_8-darkgrid")
sns.set_palette("husl")

pd.set_option("display.max_columns", None)
pd.set_option("display.max_colwidth", 120)

print("✓ Libraries ready")


# 1. Normalize Aspect Function
def normalize_aspect(aspect):
    """
    Normalize aspect text to consolidate duplicates:
    - Lowercase
    - Remove extra whitespace
    - Remove leading/trailing punctuation
    - Plurals to singular (simple -s/-es rules)
    """
    if not aspect or not isinstance(aspect, str):
        return ""

    # Remove leading quotes/apostrophes
    aspect = aspect.strip().lstrip("'\"")

    # Lowercase
    aspect = aspect.lower()

    # Normalize whitespace
    aspect = re.sub(r"\s+", " ", aspect).strip()

    # Simple plural to singular conversion
    if len(aspect) > 4:
        if aspect.endswith("ies") and not aspect.endswith("series"):
            aspect = aspect[:-3] + "y"
        elif (
            aspect.endswith("sses")
            or aspect.endswith("xes")
            or aspect.endswith("shes")
            or aspect.endswith("ches")
        ):
            aspect = aspect[:-2]
        elif (
            aspect.endswith("s")
            and not aspect.endswith("ss")
            and not aspect.endswith("us")
        ):
            if len(aspect) > 3:
                aspect = aspect[:-1]

    return aspect


# 2. Data Cleaning Function
def clean_and_consolidate_data(aspect_df):
    """
    Clean and consolidate data for aspect analysis.
    - Normalize aspects
    - Remove NaNs and empty strings
    - Group aspects and count occurrences
    """
    # Build a clean table for grouping (no NaNs, all strings)
    tmp = aspect_df[["aspect_normalized", "aspect"]].copy()
    tmp = tmp.dropna(subset=["aspect_normalized"])  # drop rows with NaN normalized key
    tmp["aspect_normalized"] = tmp["aspect_normalized"].astype(str).str.strip()
    tmp = tmp[tmp["aspect_normalized"] != ""]  # drop empty normalized keys
    tmp["aspect"] = tmp["aspect"].apply(
        lambda v: str(v).strip() if pd.notna(v) else None
    )
    tmp = tmp.dropna(subset=["aspect"])  # drop NaN originals after cast

    # Group: collect unique, sorted variants and counts
    consolidation_examples = (
        tmp.groupby("aspect_normalized")["aspect"]
        .apply(lambda x: sorted(set(x)))
        .to_frame("original_variants")
    )
    consolidation_examples["count"] = tmp.groupby("aspect_normalized").size()
    consolidation_examples = consolidation_examples.sort_values(
        "count", ascending=False
    )

    return consolidation_examples


# 3. Aspect Analysis Function
def print_aspect_analysis(aspect_df):
    """
    Print analysis of aspect data: Top 20 normalized aspects, missing data, and distinct counts.
    """
    # Consolidate data
    consolidation_examples = clean_and_consolidate_data(aspect_df)

    # Print top 20
    for idx, row in consolidation_examples.head(20).iterrows():
        variants = row["original_variants"]
        # defensively ensure all strings (in case anything sneaks in)
        variants = [str(v) for v in variants if pd.notna(v)]
        preview = ", ".join(variants[:5]) if variants else "(no examples)"
        if len(variants) > 1:
            print(f"\n'{idx}' (n={row['count']}): {preview}")
        else:
            print(f"'{idx}' (n={row['count']}): {preview}")

    # Show missingness
    missing = aspect_df.isna().mean().sort_values(ascending=False)
    print("\nMissingness (top 10):\n", missing.head(10))

    # Show distinct counts for selected columns
    print("\nDistinct counts:")
    for col in ["review_id", "aspect", "destination", "offer", "polarity", "model"]:
        if col in aspect_df.columns:
            print(f"- {col}: {aspect_df[col].nunique()}")
