import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


class DataAnalyzer:
    def __init__(self, df):
        """
        Initialize the DataAnalyzer with the dataframe.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame containing the data to analyze.
        """
        self.df = df

    def analyze_grouped_data(self, group_col: str, stats_col: str) -> pd.DataFrame
        """
        General function to group the data and calculate statistics.
        """
        grouped = (
            self.df.groupby(group_col)
            .agg(
                {
                    "id": "count",
                    stats_col: ["mean", "std", "min", "max"],
                    "word_count": "mean",
                }
            )
            .round(2)
        )

        # Flatten multi-level columns
        grouped.columns = [
            "Review_Count",
            "Avg_Rating",
            "Rating_Std",
            "Min_Rating",
            "Max_Rating",
            "Avg_Word_Count",
        ]

        # Sort by review count
        grouped = grouped.sort_values("Review_Count", ascending=False)

        return grouped

    def detailed_analysis(self, group_col, stats_col, top_n=15, min_reviews=50):
        """
        Perform detailed analysis of the grouped data.
        """
        analysis = self.analyze_grouped_data(group_col, stats_col)

        # Print the top N results
        print("=" * 100)
        print(f"{group_col.upper()} ANALYSIS")
        print("=" * 100)
        print(analysis.head(top_n))

        # Find the top 3 highest rated with at least 'min_reviews' reviews
        print(
            f"\nTop 3 Highest Rated {group_col.capitalize()} (min {min_reviews} reviews):"
        )
        high_rated = (
            analysis[analysis["Review_Count"] >= min_reviews]
            .sort_values("Avg_Rating", ascending=False)
            .head(3)
        )
        print(high_rated)


class Plotter:
    def __init__(self, df):
        """
        Initialize the Plotter with the dataframe.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame containing the data to plot.
        """
        self.df = df

    def plot_heatmap(self):
        """
        Plots a heatmap showing the number of reviews for each combination of destination and offering.
        """
        # Create a crosstab between destination and offer to get the number of reviews
        dest_offer = pd.crosstab(self.df["destination"], self.df["offer"])

        # Get the top 15 destinations based on review count
        top_destinations = self.df["destination"].value_counts().head(15).index
        dest_offer_subset = dest_offer.loc[top_destinations]

        # Plot heatmap
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

    def plot_comparison_barplot(self, group_col, stats_col, title, xlabel, ylabel):
        """
        Generic function to plot comparison bar plots for either destination or offering types.
        """
        ratings = (
            self.df.groupby(group_col)[stats_col]
            .mean()
            .sort_values(ascending=False)
            .head(15)
        )

        # Plot the bar graph
        plt.figure(figsize=(10, 6))
        plt.barh(ratings.index, ratings.values, color="lightcoral")
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title, fontweight="bold")
        plt.gca().invert_yaxis()
        plt.tight_layout()
        plt.show()

    def plot_rating_comparison(self):
        """
        Plots the comparison of average ratings by destination and offering type.
        """
        # Plot for destination ratings
        self.plot_comparison_barplot(
            group_col="destination",
            stats_col="normalized_ratings",
            title="Average Ratings by Destination (Top 15)",
            xlabel="Average Rating (0-100)",
            ylabel="Destination",
        )

        # Plot for offering ratings
        self.plot_comparison_barplot(
            group_col="offer",
            stats_col="normalized_ratings",
            title="Average Ratings by Offering Type",
            xlabel="Average Rating (0-100)",
            ylabel="Offering Type",
        )
