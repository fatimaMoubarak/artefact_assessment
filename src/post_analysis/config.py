import matplotlib
import seaborn as sns

# Set the font that supports Arabic characters
matplotlib.rcParams["font.family"] = "Arial"  # Arial or Tahoma support Arabic well

# Ensure proper right-to-left rendering (important for Arabic text)
matplotlib.rcParams["axes.unicode_minus"] = False  # Handle minus sign correctly

# Set Seaborn Style for better aesthetics
sns.set_style("whitegrid")  # A clean background style with gridlines
