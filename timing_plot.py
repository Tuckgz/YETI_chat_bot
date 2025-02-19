import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Read the processed CSV file
df = pd.read_csv("timing_data.csv")

# Convert chat_bot column to lowercase for consistent matching
df["chat_bot"] = df["chat_bot"].str.lower()

# Define colors for each chatbot
colors = {"yeti": "orange", "rufus": "green", "fi": "purple"}

# Mapping to preserve original capitalization for legend
name_mapping = {"yeti": "Yeti", "rufus": "Rufus", "fi": "Fi"}

# Create a persistent figure for the combined best-fit plot (BUT DON'T SHOW IT YET)
fig_combined, ax_combined = plt.subplots(figsize=(8, 6))

# Iterate over each chatbot
for label, color in colors.items():
    subset = df[df["chat_bot"] == label].dropna(subset=["query_num", "partial_response_time", "total_response_time"])

    if subset.empty:
        print(f"Skipping {name_mapping[label]}, no data found.")
        continue  # Skip to the next chatbot

    # Ensure query_num is numeric and sort values
    subset["query_num"] = pd.to_numeric(subset["query_num"], errors="coerce")
    subset = subset.dropna(subset=["query_num"])  # Drop NaNs from conversion
    subset = subset.sort_values("query_num")  # Ensure ordered x-axis

    print(f"Processing {name_mapping[label]}: {len(subset)} entries")  # Debugging line

    # Scatter plot for individual chatbot
    fig_individual, ax_individual = plt.subplots(figsize=(8, 6))  # NEW FIGURE FOR EACH BOT
    ax_individual.scatter(subset["query_num"], subset["partial_response_time"], color=color, label=f"{name_mapping[label]} - Partial", alpha=0.6, marker="o")
    ax_individual.scatter(subset["query_num"], subset["total_response_time"], color=color, label=f"{name_mapping[label]} - Total", alpha=0.6, marker="x")

    # Best-fit line for Partial Response Time
    coeffs_partial = np.polyfit(subset["query_num"], subset["partial_response_time"], 1)
    poly_partial = np.poly1d(coeffs_partial)
    x_range = np.linspace(0, 40, 100)
    y_partial = poly_partial(x_range)
    y_partial[y_partial < 0] = 0  # Ensure non-negative values

    ax_individual.plot(x_range, y_partial, color=color, linestyle="--", label=f"Best Fit - Partial")

    # Best-fit line for Total Response Time
    coeffs_total = np.polyfit(subset["query_num"], subset["total_response_time"], 1)
    poly_total = np.poly1d(coeffs_total)
    y_total = poly_total(x_range)
    y_total[y_total < 0] = 0  # Ensure non-negative values

    ax_individual.plot(x_range, y_total, color=color, linestyle="-", label=f"Best Fit - Total")
    ax_individual.set_xlim(0, 40)
    ax_individual.set_ylim(0, 40)

    # Labels, title, legend
    ax_individual.set_xlabel("Query Number")
    ax_individual.set_ylabel("Response Time (s)")
    ax_individual.set_title(f"Response Time Trend for {name_mapping[label]}")
    ax_individual.legend()
    ax_individual.grid(True)

    # --- Add best-fit lines with filled area to the combined plot ---
    ax_combined.plot(x_range, y_partial, color=color, linestyle="--", label=f"{name_mapping[label]} - Partial")
    ax_combined.fill_between(x_range, y_partial, alpha=0.3, color=color)

# --- Only now show the combined best-fit plot ---
ax_combined.set_xlabel("Query Number")
ax_combined.set_ylabel("Response Time (s)")
ax_combined.set_title("Comparison of Partial Response Time Trends")
ax_combined.set_xlim(0, 40)
ax_combined.set_ylim(0, 40)
ax_combined.legend()
ax_combined.grid(True)

plt.show()
