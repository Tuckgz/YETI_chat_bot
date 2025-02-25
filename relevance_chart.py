import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Updated file paths
file_paths = {
    "YETI Specific": 'yeti/yeti_responses.csv',
    "YETI General": 'yeti/yeti_general_responses.csv',
    "Rufus Specific": 'rufus/rufus_responses.csv',
    "Rufus General": 'rufus/rufus_general_responses.csv',
    "Fi Specific": 'fi/fi_responses.csv',
    "Fi General": 'fi/fi_general_responses.csv'
}

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

# Dictionary to store average similarity values
company_averages = {}

# Process multiple CSVs and calculate averages
for name, file_path in file_paths.items():
    df = load_data(file_path)
    df = compute_cosine_similarity(df)
    
    # Save the results to a CSV file
    output_file = f'relevance_{file_path.replace("/", "_")}'
    df.to_csv(output_file, index=False)
    
    # Extract company name (e.g., "Yeti", "Rufus", "Fi")
    company_name = name.split()[0]
    
    # Store average similarity for this dataset
    avg_similarity = df['Cosine Similarity'].mean()
    
    # Add to combined averages
    if company_name not in company_averages:
        company_averages[company_name] = []
    company_averages[company_name].append(avg_similarity)

# Compute final company averages
final_averages = {company: np.mean(similarities) for company, similarities in company_averages.items()}

# Plot the company-wide average cosine similarities
plt.figure(figsize=(8, 5))
plt.bar(final_averages.keys(), final_averages.values(), color=['blue', 'orange', 'green'])
plt.xlabel('Company')
plt.ylabel('Average Cosine Similarity')
plt.title('Combined Cosine Similarity Averages per Company')
plt.ylim(0, 1)  # Cosine similarity ranges from 0 to 1
plt.show()
