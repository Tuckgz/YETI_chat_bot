import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Updated file paths
file1 = 'yeti/yeti_responses.csv'
file2 = 'yeti/yeti_general_responses.csv'
file3 = 'rufus/rufus_responses.csv'
file4 = 'rufus/rufus_general_responses.csv'
file5 = 'fi/fi_responses.csv'
file6 = 'fi/fi_general_responses.csv'

# Load the CSV file
def load_data(file_path):
    return pd.read_csv(file_path)

# Compute cosine similarity
def compute_cosine_similarity(df):
    vectorizer = TfidfVectorizer()
    tfidf_matrix_questions = vectorizer.fit_transform(df['question'].astype(str))
    tfidf_matrix_responses = vectorizer.transform(df['full_response'].astype(str))
    
    similarities = [cosine_similarity(q, r)[0][0] for q, r in zip(tfidf_matrix_questions, tfidf_matrix_responses)]
    df['Cosine Similarity'] = similarities
    
    return df

# Plot similarity scores
def plot_similarity(df, title):
    similarity_bins = {
        "0-0.2": len(df[(df['Cosine Similarity'] >= 0) & (df['Cosine Similarity'] < 0.2)]),
        "0.2-0.4": len(df[(df['Cosine Similarity'] >= 0.2) & (df['Cosine Similarity'] < 0.4)]),
        "0.4-0.6": len(df[(df['Cosine Similarity'] >= 0.4) & (df['Cosine Similarity'] < 0.6)]),
        "0.6-0.8": len(df[(df['Cosine Similarity'] >= 0.6) & (df['Cosine Similarity'] < 0.8)]),
        "0.8-1.0": len(df[(df['Cosine Similarity'] >= 0.8) & (df['Cosine Similarity'] <= 1.0)])
    }
    
    labels = similarity_bins.keys()
    values = similarity_bins.values()
    
    # Bar Chart
    plt.figure(figsize=(8, 5))
    plt.bar(labels, [v / len(df) * 100 for v in values])
    plt.xlabel('Cosine Similarity Range')
    plt.ylabel('Percentage of Responses')
    plt.title(f'Cosine Similarity Distribution - {title}')
    plt.show()
    
    # Pie Chart
    plt.figure(figsize=(6, 6))
    plt.pie([v / sum(values) * 100 for v in values], labels=labels, autopct=lambda p: f'{p:.0f}%', startangle=140)
    plt.title(f'Cosine Similarity Distribution - {title}')
    plt.show()

# Process multiple CSVs
for file_path in [file1, file2, file3, file4, file5, file6]:
    df = load_data(file_path)
    df = compute_cosine_similarity(df)
    
    # Save the results to a CSV file
    output_file = f'relevance_{file_path.replace("/", "_")}'
    df.to_csv(output_file, index=False)
    print(f'Results saved to {output_file}')
    
    # Plot results
    plot_similarity(df, "Yeti Specific" if "yeti_responses.csv" in file_path else "Yeti General" if "yeti_general_responses.csv" in file_path else "Rufus Specific" if "rufus_responses.csv" in file_path else "Rufus General" if "rufus_general_responses.csv" in file_path else "Fi Specific" if "fi_responses.csv" in file_path else "Fi General")
