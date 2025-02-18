import pandas as pd
import numpy as np
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
