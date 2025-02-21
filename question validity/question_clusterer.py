import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sentence_transformers import SentenceTransformer

# File paths
file_paths = {
    'yeti': 'yeti/yeti_extra_questions_cleaned.csv',
    'fi': 'fi/fi_gps_questions_cleaned.csv',
    'rufus': 'rufus/rufus_extra_questions_cleaned.csv'
}

# Load SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Function to load and encode questions
def load_and_encode(file_path):
    df = pd.read_csv(file_path)
    questions = df.iloc[:, 2].dropna().tolist()  # Column index 2 (zero-based)
    embeddings = np.array([model.encode(q) for q in questions])
    return df, questions, embeddings

# Process files
data = []
for label, path in file_paths.items():
    df, questions, embeddings = load_and_encode(path)
    data.append((label, df, questions, embeddings))

# Combine embeddings for clustering
all_embeddings = np.vstack([d[3] for d in data])

# Determine number of clusters (adjust if needed)
num_clusters = 5  

# Perform KMeans clustering
kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init=10)
clusters = kmeans.fit_predict(all_embeddings)

# Assign clusters back to original dataframes
start = 0
for label, df, questions, embeddings in data:
    end = start + len(questions)
    df['Cluster'] = clusters[start:end]
    df.to_csv(f'{label}_clustered.csv', index=False)
    start = end

print("Clustering complete. Clustered files saved.")
