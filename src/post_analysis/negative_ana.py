import matplotlib.pyplot as plt
from src.post_analysis.config import sns
from src.post_analysis.utils import display_arabic
import pandas as pd


class NegativeAnalysisVisualizer:
    def __init__(self, aspect_df):
        """
        Initializes the NegativeAnalysisVisualizer class with the given dataframe.

        :param aspect_df: DataFrame containing aspect information, including 'polarity', 'aspect_normalized', 'offer', 'destination', 'confidence', 'evidence_span', and 'month'
        """
        self.aspect_df = aspect_df
        self.pol = self.aspect_df["polarity"].astype(str).str.lower().fillna("")
        self.neg_mask = self.pol.eq("negative")

    def plot_top_negative_aspects(self):
        """Plots the top 20 most negative aspects (normalized)."""
        neg_aspects = (
            self.aspect_df[self.neg_mask]["aspect_normalized"].value_counts().head(20)
        )

        # Apply Arabic fix only to the aspect labels
        neg_aspects_ar = neg_aspects.copy()
        neg_aspects_ar.index = [display_arabic(x) for x in neg_aspects.index]

        plt.figure(figsize=(8, 6))
        sns.barplot(x=neg_aspects_ar.values, y=neg_aspects_ar.index, color="crimson")
        plt.title("Top 20 Negative Aspects (Normalized)", fontsize=16, weight="bold")
        plt.xlabel("Negative Count", fontsize=14)
        plt.ylabel("Aspect", fontsize=14)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        plt.tight_layout()
        plt.show()

    def plot_negative_share_by_offering(self, min_rows=30):
        """Plots the negative share by offering, with a minimum volume filter."""
        agg = (
            self.aspect_df.assign(is_neg=self.pol.eq("negative"))
            .groupby("offer")
            .agg(n=("is_neg", "size"), neg_share=("is_neg", "mean"))
            .query("n >= @min_rows")
            .sort_values("neg_share", ascending=False)
        )

        plt.figure(figsize=(8, 6))
        sns.barplot(
            data=agg.head(15), x="neg_share", y=agg.head(15).index, color="crimson"
        )
        plt.title("Negative Share by Offering (n ≥ 30)", fontsize=16, weight="bold")
        plt.xlabel("Negative Share", fontsize=14)
        plt.ylabel("Offering", fontsize=14)
        plt.xlim(0, 1)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        plt.tight_layout()
        plt.show()

    def plot_negative_share_by_destination(self, min_rows=30):
        """Plots the negative share by destination, with a minimum volume filter."""
        agg_d = (
            self.aspect_df.assign(is_neg=self.pol.eq("negative"))
            .groupby("destination")
            .agg(n=("is_neg", "size"), neg_share=("is_neg", "mean"))
            .query("n >= @min_rows")
            .sort_values("neg_share", ascending=False)
        )

        plt.figure(figsize=(8, 8))
        sns.barplot(
            data=agg_d.head(20), x="neg_share", y=agg_d.head(20).index, color="crimson"
        )
        plt.title("Negative Share by Destination (n ≥ 30)", fontsize=16, weight="bold")
        plt.xlabel("Negative Share", fontsize=14)
        plt.ylabel("Destination", fontsize=14)
        plt.xlim(0, 1)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        plt.tight_layout()
        plt.show()

    def plot_negative_share_by_aspect_and_offering(self, min_mentions=5):
        """Plots a heatmap of negative share by aspect and offering."""
        # Get the top 12 most mentioned negative aspects
        focus_neg_aspects = (
            self.aspect_df[self.neg_mask]["aspect_normalized"]
            .value_counts()
            .head(12)
            .index.tolist()
        )

        # Prepare the data
        subn = self.aspect_df[
            self.aspect_df["aspect_normalized"].isin(focus_neg_aspects)
        ].copy()
        subn = subn.dropna(subset=["offer", "aspect_normalized"])
        subn["is_neg"] = subn["polarity"].astype(str).str.lower().eq("negative")

        # Calculate both count and negative share
        hmn = (
            subn.groupby(["aspect_normalized", "offer"])
            .agg(total_count=("is_neg", "size"), neg_share=("is_neg", "mean"))
            .reset_index()
        )

        # Filter out combinations with too few mentions
        hmn_filtered = hmn[hmn["total_count"] >= min_mentions].copy()

        # Apply Arabic reshaping to the aspect names for the heatmap index
        hmn_filtered["aspect_ar"] = hmn_filtered["aspect_normalized"].apply(
            display_arabic
        )

        # Pivot table with reshaped aspect labels
        pivotn = hmn_filtered.pivot_table(
            index="aspect_ar", columns="offer", values="neg_share"
        )

        # Plot the heatmap
        plt.figure(figsize=(12, 8))
        sns.heatmap(
            pivotn,
            cmap="Reds",
            vmin=0,
            vmax=1,
            annot=True,
            fmt=".2f",
            cbar_kws={"label": "Negative Share"},
            annot_kws={"size": 12, "weight": "bold", "color": "black"},
        )
        plt.title(
            f"Negative Share: Top 12 Negative Aspects by Offering (min {min_mentions} mentions)",
            fontsize=16,
            weight="bold",
        )
        plt.xlabel("Offering", fontsize=14)
        plt.ylabel("Aspect", fontsize=14)
        plt.tight_layout()
        plt.show()

    def plot_monthly_negative_share(self):
        """Plots the trend of negative share over time (by month)."""
        # Group by month and calculate the count and negative share
        by_m = (
            self.aspect_df.assign(is_neg=self.aspect_df["polarity"].eq("negative"))
            .groupby("month")
            .agg(count=("is_neg", "size"), neg_share=("is_neg", "mean"))
        )

        # Plot the bar chart and line plot with the negative share
        fig, ax1 = plt.subplots(figsize=(12, 6))

        # Bar plot for count of aspects per month
        by_m["count"].plot(kind="bar", ax=ax1, color="lightcoral", width=0.8)
        ax1.set_ylabel("Aspect Count", color="lightcoral", fontsize=14)
        ax1.set_xlabel("Month", fontsize=14)
        ax1.tick_params(axis="both", labelsize=12)

        # Add counts on top of bars
        for x, v in enumerate(by_m["count"].values):
            ax1.text(
                x, v + 2, str(v), ha="center", va="bottom", fontsize=10, color="black"
            )

        # Second y-axis for negative share line plot
        ax2 = ax1.twinx()
        ax2.plot(
            by_m.index,
            by_m["neg_share"],
            color="crimson",
            marker="o",
            markersize=6,
            linewidth=2,
        )
        ax2.set_ylabel("Negative Share", color="crimson", fontsize=14)
        ax2.set_ylim(0, 1)  # Ensure the y-axis for negative share goes from 0 to 1
        ax2.tick_params(axis="both", labelsize=12)

        # Format x-axis to show just Year-Month and remove the time part
        ax1.set_xticklabels(
            [x.strftime("%Y-%m") for x in by_m.index],
            rotation=45,
            ha="right",
            fontsize=12,
        )

        # Title and layout adjustments
        plt.title(
            "Monthly Aspect Volume and Negative Share", fontsize=16, weight="bold"
        )
        plt.tight_layout()

        # Show the plot
        plt.show()

    def generate_insights_summary(self):
        """Generates a succinct summary of insights related to negative polarity."""
        pol = self.aspect_df["polarity"].astype(str).str.lower()
        neg_aspect_counts = self.aspect_df[pol.eq("negative")][
            "aspect_normalized"
        ].value_counts()

        MIN_ROWS = 30
        neg_by_off = (
            self.aspect_df.assign(is_neg=pol.eq("negative"))
            .groupby("offer")
            .agg(n=("is_neg", "size"), neg_share=("is_neg", "mean"))
            .query("n >= @MIN_ROWS")
            .sort_values("neg_share", ascending=False)
        )
        neg_by_dest = (
            self.aspect_df.assign(is_neg=pol.eq("negative"))
            .groupby("destination")
            .agg(n=("is_neg", "size"), neg_share=("is_neg", "mean"))
            .query("n >= @MIN_ROWS")
            .sort_values("neg_share", ascending=False)
        )

        by_m = (
            self.aspect_df.assign(is_neg=pol.eq("negative"))
            .groupby(
                pd.to_datetime(self.aspect_df["date"])
                .dt.to_period("M")
                .dt.to_timestamp()
            )
            .agg(count=("is_neg", "size"), neg_share=("is_neg", "mean"))
        )

        def pct(x):
            return f"{100 * x:.1f}%"

        lines = []
        lines.append(
            f"Top negative aspects: {', '.join(neg_aspect_counts.head(5).index.tolist())}"
        )
        if not neg_by_off.empty:
            lines.append(
                f"Offerings with highest negative share (n≥{MIN_ROWS}): "
                + ", ".join(
                    [
                        f"{idx} ({pct(row.neg_share)})"
                        for idx, row in neg_by_off.head(5).iterrows()
                    ]
                )
            )
        if not neg_by_dest.empty:
            lines.append(
                f"Destinations with highest negative share (n≥{MIN_ROWS}): "
                + ", ".join(
                    [
                        f"{idx} ({pct(row.neg_share)})"
                        for idx, row in neg_by_dest.head(5).iterrows()
                    ]
                )
            )

        print("\n".join(lines))

    def plot_all(self):
        """Generates all negative analysis visualizations and insights summary."""
        self.plot_top_negative_aspects()
        self.plot_negative_share_by_offering()
        self.plot_negative_share_by_destination()
        self.plot_negative_share_by_aspect_and_offering()
        self.plot_monthly_negative_share()
        self.generate_insights_summary()
