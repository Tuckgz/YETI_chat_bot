import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from textblob import TextBlob
import re

# Load chatbot response CSVs
yeti_responses_file = "yeti_responses.csv"
rufus_responses_file = "rufus_responses.csv"

# Load chatbot question CSVs
yeti_questions_file = "yeti_questions.csv"
rufus_questions_file = "rufus_questions.csv"

# Load the datasets
yeti_responses_df = pd.read_csv(yeti_responses_file)
rufus_responses_df = pd.read_csv(rufus_responses_file)
yeti_questions_df = pd.read_csv(yeti_questions_file)
rufus_questions_df = pd.read_csv(rufus_questions_file)

# Function to detect redirects
def contains_redirect(response):
    return bool(re.search(r'https?://|click here|visit our website|find out more|Explore the page|See more details|Click below|link', 
                          response, re.IGNORECASE))

# Function to detect misunderstandings
def contains_does_not_understand(response):
    return bool(re.search(r"(I don't understand|Can you rephrase|Sorry|Could you clarify|I'm not sure|I didn't get that|please reword|any inquiries|i don't have an answer|i'm here to assist|sorry)", 
                          response, re.IGNORECASE))

# Function to compute sentiment score
def get_sentiment(response):
    return TextBlob(response).sentiment.polarity  # Ranges from -1 (negative) to 1 (positive)

# Function to analyze chatbot helpfulness
def analyze_helpfulness(df):
    if df.empty:
        return pd.DataFrame()
    
    vectorizer = CountVectorizer().fit_transform(df['full_response'])
    cos_sim_matrix = cosine_similarity(vectorizer)
    
    df['variation_penalty'] = [1 - np.mean(cos_sim_matrix[i]) for i in range(len(df))]
    df['has_redirect'] = df['full_response'].apply(contains_redirect)
    df['does_not_understand'] = df['full_response'].apply(contains_does_not_understand)
    df['sentiment_score'] = df['full_response'].apply(get_sentiment)
    
    # Normalize response time (assuming lower response time is better)
    if 'response_time' in df.columns:
        min_time = df['response_time'].min()
        max_time = df['response_time'].max()
        df['response_time_penalty'] = (df['response_time'] - min_time) / (max_time - min_time)
    else:
        df['response_time_penalty'] = 0  # Default if column not found
    
    # Compute helpfulness score factoring in misunderstandings, redirections, and sentiment positively
    df['helpfulness_score'] = (df['variation_penalty'] - 
                               (df['has_redirect'] * 0.5) - 
                               (df['does_not_understand'] * 0.5) - 
                               df['response_time_penalty'] +
                               (df['sentiment_score'] * 0.5))  # Positive sentiment improves score
    
    min_score = df['helpfulness_score'].min()
    max_score = df['helpfulness_score'].max()
    if max_score > min_score:
        df['helpfulness_score'] = (df['helpfulness_score'] - min_score) / (max_score - min_score)
    else:
        df['helpfulness_score'] = 0.5
    
    summary = pd.DataFrame({
        'Average Helpfulness Score': [df['helpfulness_score'].mean()],
        'Variation Penalty (Lower Similarity is Better)': [df['variation_penalty'].mean()],
        'Redirect Frequency': [df['has_redirect'].mean()],
        'Misunderstanding Frequency': [df['does_not_understand'].mean()],
        'Response Time Penalty': [df['response_time_penalty'].mean()],
        'Average Sentiment Score': [df['sentiment_score'].mean()]
    })
    
    return summary

# Analyze each chatbot independently
yeti_results = analyze_helpfulness(yeti_responses_df)
rufus_results = analyze_helpfulness(rufus_responses_df)

# Combine results for comparison
comparison_df = pd.concat([yeti_results, rufus_results], ignore_index=True)
comparison_df.index = ['Yeti', 'Rufus']  # Label rows

# Display the updated results
print("\nChatbot Helpfulness Comparison:")
pd.set_option('display.max_rows', None)  # Show all rows
pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.expand_frame_repr', False)  # Prevent line wrapping
pd.set_option('display.float_format', '{:.6f}'.format)  # Improve float precision
print(comparison_df)

# Save the updated results to CSV
comparison_df.to_csv('chatbot_helpfulness_comparison.csv', index=True)

print("\nComparison results saved to 'chatbot_helpfulness_comparison.csv'")

# Visualization: Pie Chart for Response Types
response_types = ['Helpful Responses', 'Redirects', 'Misunderstandings']
yeti_counts = [
    len(yeti_responses_df) - yeti_responses_df['has_redirect'].sum() - yeti_responses_df['does_not_understand'].sum(),
    yeti_responses_df['has_redirect'].sum(),
    yeti_responses_df['does_not_understand'].sum()
]
yeti_sentiment = yeti_responses_df['sentiment_score'].mean()

rufus_counts = [
    len(rufus_responses_df) - rufus_responses_df['has_redirect'].sum() - rufus_responses_df['does_not_understand'].sum(),
    rufus_responses_df['has_redirect'].sum(),
    rufus_responses_df['does_not_understand'].sum()
]
rufus_sentiment = rufus_responses_df['sentiment_score'].mean()

fig, axes = plt.subplots(1, 2, figsize=(12, 6))
axes[0].pie(yeti_counts, labels=response_types, autopct='%1.1f%%', startangle=140)
axes[0].set_title('Yeti Response Distribution')
axes[0].text(0, -1.5, f'Sentiment Score: {yeti_sentiment:.2f} (Higher = Happier)', ha='center', fontsize=12)
axes[1].pie(rufus_counts, labels=response_types, autopct='%1.1f%%', startangle=140)
axes[1].set_title('Rufus Response Distribution')
axes[1].text(0, -1.5, f'Sentiment Score: {rufus_sentiment:.2f} (Higher = Happier)', ha='center', fontsize=12)
plt.show()

# Visualization: Bar Chart for Helpfulness Score
fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(comparison_df.index, comparison_df['Average Helpfulness Score'], color='blue', edgecolor='black')
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, height, f'{height:.2f}', ha='center', va='bottom', fontsize=12, fontweight='bold', color='black')
ax.set_xlabel('Chatbots')
ax.set_ylabel('Helpfulness Score (0-1)')
ax.set_title('Chatbot Helpfulness Score Comparison')
ax.set_ylim(0, 1)
plt.show()