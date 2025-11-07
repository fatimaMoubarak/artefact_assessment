import matplotlib.pyplot as plt

# Import required libraries
import pandas as pd
import seaborn as sns
import warnings

warnings.filterwarnings("ignore")

# Set style for better visualizations
plt.style.use("seaborn-v0_8-darkgrid")
sns.set_palette("husl")

# Configure display options
pd.set_option("display.max_columns", None)
pd.set_option("display.max_colwidth", 100)

print("✓ Libraries imported successfully")


def plot_language_distribution(df):
    # Get language counts
    lang_counts = df["language"].value_counts()

    # Plot the pie chart
    plt.figure(figsize=(8, 6))
    plt.pie(
        lang_counts.values,
        labels=["Arabic", "English"],
        autopct="%1.1f%%",
        colors=["#647B8F", "#697675"],
        startangle=90,
        explode=(0.05, 0.05),
        shadow=True,
        textprops={"fontsize": 12, "fontweight": "bold"},
    )
    plt.title("Language Distribution", fontsize=14, fontweight="bold", pad=20)
    plt.tight_layout()
    plt.show()

    # Print the counts and percentages
    arabic_reviews = lang_counts.get("ara", 0)
    english_reviews = lang_counts.get("eng", 0)

    total_reviews = len(df)

    print(
        f"Arabic reviews: {arabic_reviews:,} ({(arabic_reviews/total_reviews)*100:.1f}%)"
    )
    print(
        f"English reviews: {english_reviews:,} ({(english_reviews/total_reviews)*100:.1f}%)"
    )


def plot_rating_distribution(df):
    # Create subplots for the box plot and histogram
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    # Box plot
    bp = axes[0].boxplot(
        [df["normalized_ratings"].dropna()],
        vert=True,
        patch_artist=True,
        boxprops=dict(facecolor="lightblue", alpha=0.7),
        medianprops=dict(color="red", linewidth=2),
        whiskerprops=dict(linewidth=1.5),
        capprops=dict(linewidth=1.5),
        flierprops=dict(marker="o", markerfacecolor="red", markersize=5, alpha=0.5),
    )
    axes[0].set_ylabel("Rating (Normalized 0-100)", fontsize=12)
    axes[0].set_title("Rating Distribution (Box Plot)", fontweight="bold", fontsize=14)
    axes[0].grid(axis="y", alpha=0.3)
    axes[0].set_xticklabels(["All Reviews"])

    # Histogram with KDE
    axes[1].hist(
        df["normalized_ratings"],
        bins=20,
        color="steelblue",
        alpha=0.7,
        edgecolor="black",
    )
    axes[1].axvline(
        df["normalized_ratings"].mean(),
        color="red",
        linestyle="--",
        linewidth=2,
        label=f'Mean: {df["normalized_ratings"].mean():.1f}',
    )
    axes[1].axvline(
        df["normalized_ratings"].median(),
        color="green",
        linestyle="--",
        linewidth=2,
        label=f'Median: {df["normalized_ratings"].median():.1f}',
    )
    axes[1].set_xlabel("Rating (Normalized 0-100)", fontsize=12)
    axes[1].set_ylabel("Frequency", fontsize=12)
    axes[1].set_title("Rating Distribution (Histogram)", fontweight="bold", fontsize=14)
    axes[1].legend(fontsize=10)
    axes[1].grid(axis="y", alpha=0.3)

    # Adjust layout to make space for the plots
    plt.tight_layout()
    plt.show()

    # Print statistics
    print(f"Mean rating: {df['normalized_ratings'].mean():.2f}")
    print(f"Median rating: {df['normalized_ratings'].median():.2f}")
    print(f"Std deviation: {df['normalized_ratings'].std():.2f}")


def plot_top_10_destinations(df):
    # Get the top 10 destinations by review count
    dest_counts = df["destination"].value_counts().head(10)

    # Create a horizontal bar plot
    plt.figure(figsize=(12, 7))
    bars = plt.barh(
        range(len(dest_counts)),
        dest_counts.values,
        color="coral",
        edgecolor="darkred",
        alpha=0.8,
    )
    plt.yticks(range(len(dest_counts)), dest_counts.index, fontsize=11)
    plt.xlabel("Number of Reviews", fontsize=12, fontweight="bold")
    plt.title(
        "Top 10 Destinations by Review Count", fontweight="bold", fontsize=14, pad=15
    )
    plt.gca().invert_yaxis()  # Invert y-axis to show the top destination at the top
    plt.grid(axis="x", alpha=0.3)

    # Add value labels on bars
    for i, (bar, count) in enumerate(zip(bars, dest_counts.values)):
        plt.text(
            count + 20, i, f"{count:,}", va="center", fontsize=10, fontweight="bold"
        )

    # Adjust layout and show plot
    plt.tight_layout()
    plt.show()


def plot_offering_distribution(df):
    # Get the count of each offering type
    offer_counts = df["offer"].value_counts()

    # Create a bar plot
    plt.figure(figsize=(12, 7))
    colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7", "#DFE6E9"]
    bars = plt.bar(
        range(len(offer_counts)),
        offer_counts.values,
        color=colors[: len(offer_counts)],
        edgecolor="black",
        alpha=0.8,
    )

    # Set x-ticks and labels
    plt.xticks(
        range(len(offer_counts)),
        offer_counts.index,
        rotation=45,
        ha="right",
        fontsize=11,
    )
    plt.ylabel("Number of Reviews", fontsize=12, fontweight="bold")
    plt.title("Reviews by Offering Type", fontweight="bold", fontsize=14, pad=15)
    plt.grid(axis="y", alpha=0.3)

    # Add value labels on the bars
    for bar, count in zip(bars, offer_counts.values):
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2.0,
            height + 50,
            f"{count:,}",
            ha="center",
            va="bottom",
            fontsize=10,
            fontweight="bold",
        )

    # Adjust layout and display the plot
    plt.tight_layout()
    plt.show()


def plot_word_count_distribution(df):
    # Create a figure for the histogram
    fig, axes = plt.subplots(1, figsize=(16, 6))

    # Zoomed in on the main concentration (0-100 words)
    axes.hist(
        df[df["word_count"] <= 100]["word_count"],
        bins=50,
        color="mediumpurple",
        alpha=0.7,
        edgecolor="black",
    )

    # Plot the median and mean lines
    axes.axvline(
        df["word_count"].median(),
        color="red",
        linestyle="--",
        linewidth=2,
        label=f'Median: {df["word_count"].median():.0f}',
    )
    axes.axvline(
        df["word_count"].mean(),
        color="green",
        linestyle="--",
        linewidth=2,
        label=f'Mean: {df["word_count"].mean():.1f}',
    )

    # Labels and title
    axes.set_xlabel("Word Count", fontsize=12, fontweight="bold")
    axes.set_ylabel("Frequency", fontsize=12, fontweight="bold")
    axes.set_title(
        "Review Length Distribution (0-100 words, zoomed)",
        fontweight="bold",
        fontsize=14,
    )
    axes.legend(fontsize=11)
    axes.grid(axis="y", alpha=0.3)

    # Adjust layout and display the plot
    plt.tight_layout()
    plt.show()

    # Calculate and print statistics
    percentile_95 = df["word_count"].quantile(0.95)

    print(f"Average word count: {df['word_count'].mean():.1f}")
    print(f"Median word count: {df['word_count'].median():.0f}")
    print(f"Max word count: {df['word_count'].max()}")
    print(f"Min word count: {df['word_count'].min()}")
    print(f"95th percentile: {percentile_95:.0f}")
    print(
        f"% of reviews with ≤100 words: {(df['word_count'] <= 100).sum() / len(df) * 100:.1f}%"
    )


def plot_reviews_over_time(df):
    # Convert the 'date' column to datetime format and create a 'year_month' period column
    df["date"] = pd.to_datetime(df["date"])
    df["year_month"] = df["date"].dt.to_period("M")

    # Calculate the number of reviews per month
    time_dist = df["year_month"].value_counts().sort_index()

    # Create the plot
    plt.figure(figsize=(16, 7))
    plt.plot(
        range(len(time_dist)),
        time_dist.values,
        marker="o",
        color="darkgreen",
        linewidth=2,
        markersize=6,
        markerfacecolor="lightgreen",
        markeredgecolor="darkgreen",
        markeredgewidth=2,
    )
    plt.fill_between(
        range(len(time_dist)), time_dist.values, alpha=0.3, color="lightgreen"
    )

    # Add value labels on each point
    for i, value in enumerate(time_dist.values):
        plt.text(
            i,
            value + 10,
            str(value),
            ha="center",
            va="bottom",
            fontsize=14,
            fontweight="bold",
        )

    # Customize the plot with labels and title
    plt.xlabel("Time Period", fontsize=12, fontweight="bold")
    plt.ylabel("Number of Reviews", fontsize=12, fontweight="bold")
    plt.title("Reviews Over Time", fontweight="bold", fontsize=14, pad=15)
    plt.grid(True, alpha=0.3)

    # Set x-axis labels (sample every few to avoid crowding)
    tick_spacing = max(1, len(time_dist) // 10)
    plt.xticks(
        range(0, len(time_dist), tick_spacing),
        [str(time_dist.index[i]) for i in range(0, len(time_dist), tick_spacing)],
        rotation=45,
        ha="right",
        fontsize=9,
    )

    # Adjust layout and show the plot
    plt.tight_layout()
    plt.show()

    # Print statistics
    print(f"Date range: {time_dist.index[0]} to {time_dist.index[-1]}")
    print(f"Peak month: {time_dist.idxmax()} with {time_dist.max():,} reviews")
    print(f"Average reviews per month: {time_dist.mean():.0f}")
