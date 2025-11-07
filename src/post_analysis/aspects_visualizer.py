import matplotlib.pyplot as plt
from src.post_analysis.config import sns
from src.post_analysis.utils import display_arabic
import pandas as pd


class AspectAnalysisself:
    def __init__(self, aspect_df):
        """
        Initializes the AspectAnalysisself class with the given dataframe.

        :param aspect_df: DataFrame containing aspect information, including 'aspect_normalized', 'polarity', 'offer', 'destination'
        """
        self.aspect_df = aspect_df

    def plot_aspect_mentions(self):
        """Plots the aspect mentions by offering and destination."""
        # Aspect counts by offering and destination
        by_offering = (
            self.aspect_df.groupby("offer").size().sort_values(ascending=False).head(15)
        )
        by_destination = (
            self.aspect_df.groupby("destination")
            .size()
            .sort_values(ascending=False)
            .head(20)
        )

        fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharey=True)

        # Aspect Mentions by Offering (Top 15)
        sns.barplot(
            x=by_offering.values, y=by_offering.index, ax=axes[0], palette="Blues_d"
        )
        axes[0].set_title("Aspect Mentions by Offering (Top 15)", fontsize=16)
        axes[0].set_xlabel("Count", fontsize=14)
        axes[0].set_ylabel("Offering", fontsize=14)
        axes[0].tick_params(axis="both", labelsize=12)

        # Aspect Mentions by Destination (Top 20)
        sns.barplot(
            x=by_destination.values,
            y=by_destination.index,
            ax=axes[1],
            palette="Blues_d",
        )
        axes[1].set_title("Aspect Mentions by Destination (Top 20)", fontsize=16)
        axes[1].set_xlabel("Count", fontsize=14)
        axes[1].set_ylabel("Destination", fontsize=14)
        axes[1].tick_params(axis="both", labelsize=12)

        plt.tight_layout()
        plt.show()

    def plot_positivity_rate(self):
        """Plots the positivity rate by offering and destination."""

        # Positivity rate calculation function
        def positivity_rate(g):
            return g["polarity"].astype(str).str.lower().eq("positive").mean()

        pos_by_off = (
            self.aspect_df.groupby("offer")
            .apply(positivity_rate)
            .sort_values(ascending=False)
        )
        pos_by_dest = (
            self.aspect_df.groupby("destination")
            .apply(positivity_rate)
            .sort_values(ascending=False)
        )

        fig, axes = plt.subplots(1, 2, figsize=(14, 6))

        # Positivity Rate by Offering (Top 15)
        sns.barplot(
            x=pos_by_off.head(15).values,
            y=pos_by_off.head(15).index,
            ax=axes[0],
            palette="coolwarm",
        )
        axes[0].set_title("Positivity Rate by Offering (Top 15)", fontsize=16)
        axes[0].set_xlabel("Positive Share", fontsize=14)
        axes[0].set_xlim(0, 1)
        axes[0].tick_params(axis="both", labelsize=12)

        # Positivity Rate by Destination (Top 20)
        sns.barplot(
            x=pos_by_dest.head(20).values,
            y=pos_by_dest.head(20).index,
            ax=axes[1],
            palette="coolwarm",
        )
        axes[1].set_title("Positivity Rate by Destination (Top 20)", fontsize=16)
        axes[1].set_xlabel("Positive Share", fontsize=14)
        axes[1].set_xlim(0, 1)
        axes[1].tick_params(axis="both", labelsize=12)

        plt.tight_layout()
        plt.show()

    def plot_polarity_share_heatmap(self):
        """Plots the heatmap of polarity share by offering and aspect (top 12 normalized aspects)."""
        # Get the top 12 most normalized aspects
        focus_aspects = (
            self.aspect_df["aspect_normalized"].value_counts().head(12).index.tolist()
        )
        sub = self.aspect_df[
            self.aspect_df["aspect_normalized"].isin(focus_aspects)
        ].copy()
        sub = sub.dropna(subset=["offer", "aspect_normalized", "polarity"])
        sub["polarity"] = sub["polarity"].astype(str).str.lower()

        # Apply Arabic reshaping only to aspect labels
        sub["aspect_ar"] = sub["aspect_normalized"].apply(display_arabic)

        hm_counts = (
            sub.groupby(["offer", "aspect_ar", "polarity"]).size().reset_index(name="n")
        )
        hm_counts["share"] = hm_counts["n"] / hm_counts.groupby(["offer", "aspect_ar"])[
            "n"
        ].transform("sum")

        pivot = hm_counts.pivot_table(
            index=["offer", "aspect_ar"],
            columns="polarity",
            values="share",
            fill_value=0,
        )

        # Keep polarity column order if present
        pol_order = ["positive", "neutral", "negative"]
        existing = [c for c in pol_order if c in pivot.columns]
        pivot = pivot.reindex(
            columns=existing + [c for c in pivot.columns if c not in existing]
        )

        # Plot the heatmap
        plt.figure(figsize=(14, 10))
        ax = sns.heatmap(
            pivot,
            cmap="Blues",
            annot=True,
            fmt=".2f",
            linewidths=0.7,
            linecolor="white",
            cbar_kws={"label": "Polarity Share"},
            annot_kws={"size": 12, "weight": "bold", "color": "black"},
        )
        plt.title(
            "Polarity Share by Offering and Aspect (Top 12 Normalized Aspects)",
            fontsize=18,
            weight="bold",
        )
        plt.tight_layout()

        # Make Arabic y-tick labels nicer (no rotation, right-aligned)
        ax.set_yticklabels(ax.get_yticklabels(), rotation=0)
        for t in ax.get_yticklabels():
            t.set_horizontalalignment("right")

        plt.show()

    def plot_monthly_positivity_share(self):
        """Plots the monthly positivity share of aspects."""
        # Normalize the 'date' to month-period
        self.aspect_df["month"] = (
            pd.to_datetime(self.aspect_df["date"]).dt.to_period("M").dt.to_timestamp()
        )

        # Group by month and calculate the counts and positive share
        by_month = self.aspect_df.groupby("month").size().rename("count").to_frame()

        # Calculate the share of 'positive' aspects for each month
        by_month["positive_share"] = self.aspect_df.groupby("month")["polarity"].apply(
            lambda s: s.str.lower().eq("positive").mean()  # Calculate positivity share
        )

        # Create the plot with two y-axes
        fig, ax1 = plt.subplots(figsize=(12, 6))

        # Bar plot for count of aspects per month (count of all aspects)
        by_month["count"].plot(kind="bar", ax=ax1, color="steelblue", width=0.8)
        ax1.set_ylabel("Aspect Count", color="steelblue", fontsize=14)
        ax1.set_xlabel("Month", fontsize=14)
        ax1.tick_params(axis="both", labelsize=12)

        # Annotations for bars: adding the count on top of each bar
        for x, v in enumerate(by_month["count"].values):
            ax1.text(
                x, v + 2, str(v), ha="center", va="bottom", fontsize=10, color="black"
            )

        # Create the second y-axis for positive share
        ax2 = ax1.twinx()
        ax2.plot(
            by_month.index,
            by_month["positive_share"],
            color="darkorange",
            marker="o",
            markersize=6,
            linewidth=2,
        )
        ax2.set_ylabel("Positive Share", color="darkorange", fontsize=14)
        ax2.set_ylim(0, 1)  # Ensure the y-axis for positivity share goes from 0 to 1
        ax2.tick_params(axis="both", labelsize=12)

        # Format x-axis labels to show months properly
        ax1.set_xticks(range(len(by_month)))  # Ensure months are evenly spaced
        ax1.set_xticklabels(
            by_month.index.strftime("%b %Y"), rotation=45, ha="right", fontsize=12
        )

        # Title of the plot
        plt.title(
            "Monthly Aspect Volume and Positivity Rate", fontsize=16, weight="bold"
        )

        # Adjust layout for better fitting
        plt.tight_layout()

        # Show the plot
        plt.show()

    def plot_all(self):
        """Generates all plots: aspect mentions, positivity rate, and polarity share heatmap."""
        # Generate the plots
        self.plot_aspect_mentions()
        self.plot_positivity_rate()
        self.plot_polarity_share_heatmap()
        self.plot_monthly_positivity_share()
