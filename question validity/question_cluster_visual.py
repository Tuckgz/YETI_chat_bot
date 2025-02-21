import pandas as pd
import plotly.express as px
from sklearn.decomposition import PCA
from sentence_transformers import SentenceTransformer

# Load the clustered CSV files (update file paths accordingly)
df_yeti = pd.read_csv('yeti_clustered.csv')
df_rufus = pd.read_csv('rufus_clustered.csv')
df_fi = pd.read_csv('fi_clustered.csv')

# Initialize SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')

# Generate embeddings for the cleaned questions and store as lists of embeddings
df_yeti['embedding'] = df_yeti['cleaned_question'].apply(lambda x: model.encode(x))
df_rufus['embedding'] = df_rufus['cleaned_question'].apply(lambda x: model.encode(x))
df_fi['embedding'] = df_fi['cleaned_question'].apply(lambda x: model.encode(x))

# Combine all datasets into one for clustering visualization
all_embeddings = pd.concat([df_yeti[['embedding', 'Cluster', 'Question']], 
                            df_rufus[['embedding', 'Cluster', 'Question']], 
                            df_fi[['embedding', 'Cluster', 'Question']]])

# Extract the embeddings as a 2D array
embedding_list = [embedding for embedding in all_embeddings['embedding']]

# Perform PCA for dimensionality reduction (reduce to 2D for visualization)
pca = PCA(n_components=2)
reduced_embeddings = pca.fit_transform(embedding_list)  # PCA expects a 2D array

# Create a new DataFrame with the reduced embeddings
reduced_df = pd.DataFrame(reduced_embeddings, columns=['PCA1', 'PCA2'])
reduced_df['Cluster'] = all_embeddings['Cluster'].reset_index(drop=True)
reduced_df['Question'] = all_embeddings['Question'].reset_index(drop=True)

# Create an interactive scatter plot with Plotly
fig = px.scatter(reduced_df, x='PCA1', y='PCA2', color='Cluster', hover_data=['Question'],
                 title="Clustering of Questions Based on Embeddings (PCA)")

# Show the plot
fig.show()
