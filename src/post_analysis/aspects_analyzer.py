from src.post_analysis.utils import display_arabic
import matplotlib.pyplot as plt
from src.post_analysis.config import sns


class AspectVisualization:
    def __init__(self, aspect_df):
        """
        Initializes the AspectVisualization class with the given dataframe.

        :param aspect_df: DataFrame containing aspect information, including 'aspect_normalized' and 'polarity'
        """
        self.aspect_df = aspect_df
        self.top_aspects = self.aspect_df["aspect_normalized"].value_counts().head(20)
        self.absa_df = self.aspect_df.loc[self.aspect_df.model == "pyabsa-multilingual"]

    def plot_polarity_distribution(self):
        """Plots the distribution of polarity in the ABSA dataset."""
        plt.figure(figsize=(10, 6))
        sns.countplot(
            data=self.absa_df,
            x="polarity",
            order=self.absa_df["polarity"].value_counts().index,
            palette="viridis",
        )
        plt.title("Aspect Polarity Distribution (ABSA)", fontsize=16)
        plt.xlabel("Polarity", fontsize=14)
        plt.ylabel("Count", fontsize=14)
        plt.show()

    def plot_top_aspects(self):
        """Plots the most mentioned 20 aspects (normalized) from the aspect dataset."""
        # Apply Arabic fix only to aspect labels (index)
        top_aspects_ar = self.top_aspects.copy()
        top_aspects_ar.index = [display_arabic(x) for x in self.top_aspects.index]

        plt.figure(figsize=(10, 6))
        sns.barplot(x=top_aspects_ar.values, y=top_aspects_ar.index, palette="Blues_d")
        plt.title("Most mentioned 20 Aspects (normalized)", fontsize=16)
        plt.xlabel("Count", fontsize=14)
        plt.ylabel("Aspect", fontsize=14)
        plt.xticks(rotation=0, fontsize=12)
        plt.tight_layout()
        plt.show()

    def plot_polarity_by_top_aspects(self):
        """Plots the polarity distribution by the most mentioned aspects."""
        top_list = set(self.top_aspects.index)
        sub = self.aspect_df[self.aspect_df["aspect_normalized"].isin(top_list)].copy()

        # Add a reshaped version just for display
        sub["aspect_ar"] = sub["aspect_normalized"].apply(display_arabic)

        plt.figure(figsize=(12, 8))
        sns.countplot(
            data=sub,
            y="aspect_ar",
            hue="polarity",
            order=[display_arabic(x) for x in self.top_aspects.index],
            palette="Set2",
        )
        plt.title("Polarity by most mentioned aspects", fontsize=16)
        plt.xlabel("Count", fontsize=14)
        plt.ylabel("Aspect", fontsize=14)
        plt.legend(
            title="Polarity", bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=12
        )
        plt.tight_layout()
        plt.show()

    def plot_all(self):
        """Run all plots together."""
        self.plot_polarity_distribution()
        self.plot_top_aspects()
        self.plot_polarity_by_top_aspects()
