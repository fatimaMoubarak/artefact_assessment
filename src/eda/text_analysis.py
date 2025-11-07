import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud


class ReviewAnalysis:
    def __init__(self, df):
        """
        Initializes the ReviewAnalysis class with the provided DataFrame.

        :param df: DataFrame containing review data, including a 'tokens' column.
        """
        self.df = df

    def extract_most_common_words(self):
        """
        Extracts and returns the most common words across all reviews.
        """
        # Extract all tokens from the 'tokens' column
        all_tokens = [token for tokens in self.df["tokens"] for token in tokens]

        # Count the frequency of each word using Counter
        word_freq = Counter(all_tokens)

        # Get the 10 most common words
        most_common = word_freq.most_common(10)

        # Print the top 10 most common words
        print("=" * 100)
        print("TOP 10 MOST COMMON WORDS ACROSS ALL REVIEWS")
        print("=" * 100)
        for i, (word, count) in enumerate(most_common, 1):
            print(f"{i:2d}. {word:20s} - {count:,} occurrences")

        # Create a DataFrame for easier analysis of the most common words
        common_words_df = pd.DataFrame(most_common, columns=["Word", "Frequency"])

        # Return the DataFrame for further analysis
        return common_words_df

    def visualize_top_words(self):
        """
        Visualizes the top words using both a bar chart and a word cloud.
        """
        # Extract all tokens from the 'tokens' column and count word frequencies
        all_tokens = [token for tokens in self.df["tokens"] for token in tokens]
        word_freq = Counter(all_tokens)

        # Get the 10 most common words
        most_common = word_freq.most_common(10)

        # Create a DataFrame for easier analysis
        common_words_df = pd.DataFrame(most_common, columns=["Word", "Frequency"])

        # Visualize top words: create a figure with subplots
        fig, axes = plt.subplots(1, 2, figsize=(18, 6))

        # Bar chart of top 10 words
        axes[0].barh(
            range(len(common_words_df)), common_words_df["Frequency"], color="skyblue"
        )
        axes[0].set_yticks(range(len(common_words_df)))
        axes[0].set_yticklabels(common_words_df["Word"])
        axes[0].set_xlabel("Frequency", fontsize=12)
        axes[0].set_title(
            "Top 10 Most Common Words in Reviews", fontsize=14, fontweight="bold"
        )
        axes[0].invert_yaxis()
        axes[0].grid(axis="x", alpha=0.3)

        # Word cloud generation
        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color="white",
            colormap="viridis",
            max_words=100,
            font_path="C:/Windows/Fonts/arial.ttf",
        ).generate_from_frequencies(word_freq)

        # Display the word cloud
        axes[1].imshow(wordcloud, interpolation="bilinear")
        axes[1].axis("off")
        axes[1].set_title(
            "Word Cloud of Most Common Terms", fontsize=14, fontweight="bold"
        )

        # Adjust layout to make sure everything fits
        plt.tight_layout()
        plt.show()

        return common_words_df

    def get_top_words_by_category(self, category_column, category_value, top_n=20):
        """
        Extracts the top words for a specific category (e.g., offering type or destination).

        :param category_column: The column name to filter by (e.g., 'offer', 'destination')
        :param category_value: The value within the column to filter by (e.g., 'hotel', 'Paris')
        :param top_n: The number of top words to return (default is 20)
        """
        # Filter the DataFrame for the specific category (offering type)
        subset = self.df[self.df[category_column] == category_value]

        # Extract all tokens from the 'tokens' column
        tokens = [token for tokens in subset["tokens"] for token in tokens]

        # Count the frequency of each word using Counter
        return Counter(tokens).most_common(top_n)

    def keyword_analysis(self, category_column, top_n=5, top_words_count=15):
        """
        Performs keyword analysis for a specific category column (e.g., offering type or destination).

        :param category_column: The column name to analyze (e.g., 'offer' or 'destination')
        :param top_n: Number of top categories to analyze (default is 5)
        :param top_words_count: Number of top words to extract per category (default is 15)
        """
        print("=" * 100)
        print(f"TOP KEYWORDS BY {category_column.upper()}")
        print("=" * 100)

        # Loop through the top 'n' categories based on review count
        for category_value in self.df[category_column].value_counts().head(top_n).index:
            print(f"\n{category_value.upper()}:")
            print("-" * 100)

            # Get the top words for each category
            top_words = self.get_top_words_by_category(
                category_column, category_value, top_words_count
            )

            # Print the top words and their frequencies
            for i, (word, count) in enumerate(top_words, 1):
                print(f"  {i:2d}. {word:15s} ({count:,} times)")

    def generate_word_clouds_by_offering(self, top_n=4):
        """
        Generates and displays word clouds for the top 'n' offering types.

        :param top_n: The number of offering types to display (default is 4)
        """
        # Get the top 'n' most common offerings
        offerings = self.df["offer"].value_counts().head(top_n).index

        # Create subplots to display word clouds for each offering type
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        axes = axes.ravel()  # Flatten the axes array for easier iteration

        # Iterate over each offering type and generate a word cloud
        for idx, offering in enumerate(offerings):
            # Filter data for the current offering type
            subset = self.df[self.df["offer"] == offering]

            # Flatten tokens for this subset
            tokens = [token for tokens in subset["tokens"] for token in tokens]

            # Count word frequencies
            word_freq = Counter(tokens)

            # If there are tokens in the subset, generate the word cloud
            if word_freq:
                wordcloud = WordCloud(
                    width=600,
                    height=400,
                    background_color="white",
                    colormap="plasma",
                    max_words=80,
                    font_path="C:/Windows/Fonts/arial.ttf",
                ).generate_from_frequencies(dict(word_freq.most_common(100)))

                # Display word cloud for this offering type
                axes[idx].imshow(wordcloud, interpolation="bilinear")
                axes[idx].set_title(
                    f"{offering}\n({len(subset):,} reviews)",
                    fontsize=12,
                    fontweight="bold",
                )
                axes[idx].axis("off")

        # Add a main title for the figure
        plt.suptitle(
            "Word Clouds by Offering Type", fontsize=16, fontweight="bold", y=0.98
        )

        # Adjust layout to ensure titles and labels fit
        plt.tight_layout()
        plt.show()
