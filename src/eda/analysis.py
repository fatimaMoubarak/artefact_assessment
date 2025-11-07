import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def detailed_destination_analysis(df):
    # Grouping the data by 'destination' and calculating the required aggregations
    dest_analysis = (
        df.groupby("destination")
        .agg(
            {
                "id": "count",  # Count of reviews for each destination
                "normalized_ratings": [
                    "mean",
                    "std",
                    "min",
                    "max",
                ],  # Statistics for ratings
                "word_count": "mean",  # Average word count per review
            }
        )
        .round(2)
    )

    # Flattening the multi-level column names
    dest_analysis.columns = [
        "Review_Count",
        "Avg_Rating",
        "Rating_Std",
        "Min_Rating",
        "Max_Rating",
        "Avg_Word_Count",
    ]

    # Sorting the destinations by the number of reviews in descending order
    dest_analysis = dest_analysis.sort_values("Review_Count", ascending=False)

    # Printing the detailed destination analysis
    print("=" * 100)
    print("DESTINATION ANALYSIS")
    print("=" * 100)
    print(dest_analysis.head(15))  # Displaying the top 15 destinations

    # Finding the top 3 highest rated destinations with at least 50 reviews
    print("\nTop 3 Highest Rated Destinations (min 50 reviews):")
    high_rated = (
        dest_analysis[dest_analysis["Review_Count"] >= 50]
        .sort_values("Avg_Rating", ascending=False)
        .head(3)
    )
    print(high_rated)


def offering_analysis(df):
    # Grouping the data by 'offer' and calculating the required aggregations
    offering_analysis = (
        df.groupby("offer")
        .agg(
            {
                "id": "count",  # Count of reviews for each offering type
                "normalized_ratings": [
                    "mean",
                    "std",
                    "min",
                    "max",
                ],  # Statistics for ratings
                "word_count": "mean",  # Average word count per review
            }
        )
        .round(2)
    )

    # Flattening the multi-level column names
    offering_analysis.columns = [
        "Review_Count",
        "Avg_Rating",
        "Rating_Std",
        "Min_Rating",
        "Max_Rating",
        "Avg_Word_Count",
    ]

    # Sorting the offering types by the number of reviews in descending order
    offering_analysis = offering_analysis.sort_values("Review_Count", ascending=False)

    # Printing the offering type analysis
    print("\n" + "=" * 100)
    print("OFFERING TYPE ANALYSIS")
    print("=" * 100)
    print(offering_analysis)


def plot_destination_offering_heatmap(df):
    # Create a crosstab between destination and offer to get the number of reviews
    dest_offer = pd.crosstab(df["destination"], df["offer"])

    # Get the top 15 destinations based on review count
    top_destinations = df["destination"].value_counts().head(15).index

    # Subset the crosstab to only include the top 15 destinations
    dest_offer_subset = dest_offer.loc[top_destinations]

    # Create the heatmap plot
    plt.figure(figsize=(14, 10))
    sns.heatmap(
        dest_offer_subset,
        annot=True,
        fmt="d",
        cmap="YlOrRd",
        cbar_kws={"label": "Number of Reviews"},
    )
    plt.title(
        "Reviews by Destination and Offering Type (Top 15 Destinations)",
        fontsize=14,
        fontweight="bold",
        pad=20,
    )
    plt.xlabel("Offering Type", fontsize=12)
    plt.ylabel("Destination", fontsize=12)
    plt.xticks(rotation=45, ha="right")
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.show()


def plot_rating_comparison(df):
    # Create subplots for the destination and offering ratings
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    # Destination ratings: Group by 'destination' and calculate the average rating
    dest_ratings = (
        df.groupby("destination")["normalized_ratings"]
        .mean()
        .sort_values(ascending=False)
        .head(15)
    )

    # Bar plot for destination ratings
    axes[0].barh(range(len(dest_ratings)), dest_ratings.values, color="lightcoral")
    axes[0].set_yticks(range(len(dest_ratings)))
    axes[0].set_yticklabels(dest_ratings.index)
    axes[0].set_xlabel("Average Rating (0-100)")
    axes[0].set_title("Average Ratings by Destination (Top 15)", fontweight="bold")
    axes[0].invert_yaxis()
    axes[0].grid(axis="x", alpha=0.3)

    # Offering ratings: Group by 'offer' and calculate the average rating
    offering_ratings = (
        df.groupby("offer")["normalized_ratings"].mean().sort_values(ascending=False)
    )

    # Bar plot for offering ratings
    axes[1].bar(
        range(len(offering_ratings)),
        offering_ratings.values,
        color=["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7", "#DFE6E9"],
    )
    axes[1].set_xticks(range(len(offering_ratings)))
    axes[1].set_xticklabels(offering_ratings.index, rotation=45, ha="right")
    axes[1].set_ylabel("Average Rating (0-100)")
    axes[1].set_title("Average Ratings by Offering Type", fontweight="bold")
    axes[1].grid(axis="y", alpha=0.3)

    # Adjust layout and display the plot
    plt.tight_layout()
    plt.show()
