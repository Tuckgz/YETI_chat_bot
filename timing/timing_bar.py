import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Read the processed CSV file
df = pd.read_csv("timing_data.csv")

# Define chatbot color schemes (partial is darker, total is lighter)
color_schemes = {
    "yeti": ("#c27b00", "#ffa200"),  # Orange shades (dark -> light)
    "rufus": ("#6b6b6b", "#9e9e9e"),  # Gray shades (dark -> light)
    "fi": ("#71627a", "#a699b3")     # Purple-gray shades (dark -> light)
}

# Ensure correct data types
df["query_num"] = df["query_num"].astype(int)
df["partial_response_time"] = df["partial_response_time"].astype(float)
df["total_response_time"] = df["total_response_time"].astype(float)

# Group by chatbot and query number, calculating mean response times
df_grouped = df.groupby(["chat_bot", "query_num"]).agg(
    partial_mean=("partial_response_time", "mean"),
    total_mean=("total_response_time", "mean")
).reset_index()

# Get unique query numbers for X-axis
query_nums = df_grouped["query_num"].unique()
query_nums.sort()

# Bar width for grouped display
bar_width = 0.25
index = np.arange(len(query_nums))

# Create a figure
fig, ax = plt.subplots(figsize=(10, 6))

# Loop through chatbots and plot bars
for i, (label, (partial_color, total_color)) in enumerate(color_schemes.items()):
    subset = df_grouped[df_grouped["chat_bot"] == label]

    # Align with query numbers (ensuring all X values exist)
    aligned_subset = subset.set_index("query_num").reindex(query_nums).reset_index()
    
    # Replace NaN values (if chatbot is missing data for a query number)
    aligned_subset.fillna(0, inplace=True)

    # Plot partial response time (bottom layer, darker color)
    ax.bar(index + i * bar_width, aligned_subset["partial_mean"], bar_width,
           label=f"{label.capitalize()} - Partial", color=partial_color, alpha=0.9)

    # Plot total response time (stacked on top, lighter color)
    ax.bar(index + i * bar_width, aligned_subset["total_mean"], bar_width,
           label=f"{label.capitalize()} - Total", color=total_color, alpha=0.9,
           bottom=aligned_subset["partial_mean"])

# Formatting
ax.set_xlabel("Query Number")
ax.set_ylabel("Response Time (s)")
ax.set_title("Chatbot Response Time Comparison")
ax.set_xticks(index + bar_width)
ax.set_xticklabels(query_nums, rotation=45)
ax.legend()
ax.grid(axis="y", linestyle="--", alpha=0.5)

# Show the bar chart
plt.tight_layout()
plt.show()
