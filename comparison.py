import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import re

# Load chatbot CSVs separately
yeti_file = "yeti_responses.csv"  # Update with actual file path if needed
rufus_file = "rufus_responses.csv"

# Load the datasets
yeti_df = pd.read_csv(yeti_file)
rufus_df = pd.read_csv(rufus_file)

# Function to detect redirects
def contains_redirect(response):
    return bool(re.search(r'https?://|click here|visit our website|find out more|Explore the page|See more details|Click below|link', 
                          response, re.IGNORECASE))

# Function to detect misunderstandings
def contains_does_not_understand(response):
    return bool(re.search(r"(I don't understand|Can you rephrase|Sorry|Could you clarify|I'm not sure|I didn't get that|please reword|I understand you're looking for)", 
                          response, re.IGNORECASE))

# Function to analyze chatbot helpfulness independently
def analyze_helpfulness(df):
    if df.empty:
        return pd.DataFrame()  # Return an empty DataFrame if there's no data

    # Step 1: Measure Variation in Responses using Cosine Similarity
    vectorizer = CountVectorizer().fit_transform(df['full_response'])
    cos_sim_matrix = cosine_similarity(vectorizer)
    
    # Invert variation score (Lower similarity = Higher helpfulness)
    df['variation_penalty'] = [1 - np.mean(cos_sim_matrix[i]) for i in range(len(df))]

    # Step 2: Apply Redirect Detection
    df['has_redirect'] = df['full_response'].apply(contains_redirect)

    # Step 3: Apply Misunderstanding Detection
    df['does_not_understand'] = df['full_response'].apply(contains_does_not_understand)

    # Step 4: Compute Raw Helpfulness Score
    df['helpfulness_score'] = df['variation_penalty'] - df['has_redirect'] - df['does_not_understand']

    # Normalize the helpfulness score between 0 and 1
    min_score = df['helpfulness_score'].min()
    max_score = df['helpfulness_score'].max()
    if max_score > min_score:  # Avoid division by zero
        df['helpfulness_score'] = (df['helpfulness_score'] - min_score) / (max_score - min_score)
    else:
        df['helpfulness_score'] = 0.5  # Default mid-value if no variation exists

    # Compute overall chatbot performance
    summary = pd.DataFrame({
        'Average Helpfulness Score': [df['helpfulness_score'].mean()],
        'Variation Penalty (Lower Similarity is Better)': [df['variation_penalty'].mean()],
        'Redirect Frequency': [df['has_redirect'].mean()],
        'Misunderstanding Frequency': [df['does_not_understand'].mean()]
    })

    return summary

# Analyze each chatbot independently
yeti_results = analyze_helpfulness(yeti_df)
rufus_results = analyze_helpfulness(rufus_df)

# Combine results for comparison
comparison_df = pd.concat([yeti_results, rufus_results], ignore_index=True)
comparison_df.index = ['Yeti', 'Rufus']  # Label rows

# Display the updated results
print("\nChatbot Helpfulness Comparison:")
print(comparison_df)

# Save the updated results to CSV
comparison_df.to_csv('chatbot_helpfulness_comparison.csv', index=True)

print("\nComparison results saved to 'chatbot_helpfuness_comparison.csv'")

### Uncomment all below lines to see lines containing redirects to manually check ###

# print("\nYeti responses containing possible redirects (Click below or link):")
# print(yeti_df[yeti_df['full_response'].str.contains('Click below|link', case=False, na=False)])

# print("\nRufus responses containing possible redirects (link):")
# print(rufus_df[rufus_df['full_response'].str.contains('link', case=False, na=False)])

### Visualization code below ###

# Load the saved chatbot performance comparison CSV
comparison_df = pd.read_csv("chatbot_helpfulness_comparison.csv", index_col=0)

# Define metrics
helpfulness_metric = 'Average Helpfulness Score'
other_metrics = ['Variation Penalty (Lower Similarity is Better)', 'Redirect Frequency', 'Misunderstanding Frequency']

### **Bar Graph for Helpfulness Score Only**
fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(comparison_df.index, comparison_df[helpfulness_metric], color='blue', edgecolor='black')

# Add text labels on top of the bars for Helpfulness Score
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, height, f'{height:.2f}', 
            ha='center', va='bottom', fontsize=12, fontweight='bold', color='black')

# Labeling for Helpfulness Score
ax.set_xlabel('Chatbots')
ax.set_ylabel('Helpfulness Score (0-1)')
ax.set_title('Chatbot Helpfulness Score Comparison')
ax.set_ylim(0, 1)  # Ensure consistency in scaling

plt.show()

### **Grouped Bar Graph for Other Metrics**
x = np.arange(len(comparison_df.index))  # the label locations
width = 0.2  # the width of the bars

fig, ax = plt.subplots(figsize=(10, 6))

# Plot each metric as a set of bars
for i, metric in enumerate(other_metrics):
    ax.bar(x + i * width, comparison_df[metric], width, label=metric, edgecolor='black')

# Labeling
ax.set_xlabel('Chatbots')
ax.set_ylabel('Score (Normalized 0-1)')
ax.set_title('Chatbot Performance Comparison Across Metrics')
ax.set_xticks(x + width * (len(other_metrics) / 2 - 0.5))
ax.set_xticklabels(comparison_df.index)
ax.legend()

plt.show()