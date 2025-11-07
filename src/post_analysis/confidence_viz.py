import matplotlib.pyplot as plt
from src.post_analysis.config import sns


class ConfidenceEvidenceVisualizer:
    def __init__(self, aspect_df):
        """
        Initializes the ConfidenceEvidenceVisualizer class with the given dataframe.

        :param aspect_df: DataFrame containing aspect information, including 'confidence', 'evidence_span', and 'polarity'
        """
        self.aspect_df = aspect_df

    def plot_confidence_distribution(self):
        """Plots the confidence distribution."""
        plt.figure(figsize=(6, 4))
        sns.histplot(self.aspect_df["confidence"].dropna(), bins=20, kde=True)
        plt.title("Confidence Distribution", fontsize=16)
        plt.xlabel("Confidence", fontsize=14)
        plt.ylabel("Frequency", fontsize=14)
        plt.tight_layout()
        plt.show()

    def plot_evidence_length_vs_confidence(self):
        """Plots the relationship between evidence length and confidence."""
        # Create a new column for the length of the evidence span
        self.aspect_df["evidence_len"] = (
            self.aspect_df["evidence_span"].fillna("").str.len()
        )

        plt.figure(figsize=(6, 4))
        sns.scatterplot(
            data=self.aspect_df,
            x="evidence_len",
            y="confidence",
            hue="polarity",
            alpha=0.5,
        )
        plt.title("Evidence Length vs Confidence", fontsize=16)
        plt.xlabel("Evidence length (chars)", fontsize=14)
        plt.ylabel("Confidence", fontsize=14)
        plt.tight_layout()
        plt.show()

    def plot_all(self):
        """Generates all confidence and evidence visualizations."""
        self.plot_confidence_distribution()
        self.plot_evidence_length_vs_confidence()
