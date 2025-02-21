import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
import string

# Ensure NLTK stopwords are available
try:
    from nltk.corpus import stopwords
    stop_words = set(stopwords.words('english'))
except:
    nltk.download('stopwords')
    from nltk.corpus import stopwords
    stop_words = set(stopwords.words('english'))

# Load CSV files
file_paths = ['yeti/yeti_extra_questions_cleaned.csv', 'rufus/rufus_extra_questions_cleaned.csv', 'fi/fi_gps_questions_cleaned.csv']
dfs = [pd.read_csv(file) for file in file_paths]

# Ensure CSVs have at least three columns (Category, Question, and Cleaned Question)
for df in dfs:
    if len(df.columns) < 3:
        raise ValueError("Each CSV must have at least three columns: 'Category', 'Question', and 'Cleaned Question'.")

# Extract column names dynamically
category_col, question_col, cleaned_question_col = dfs[0].columns[:3]  # Use the first 3 columns

# Define the chatbot names corresponding to each dataset
chatbot_names = ['Yeti', 'Rufus', 'Fi']

# Load Sentence-BERT model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Encode questions using the 'cleaned_question' column
def get_embeddings(df):
    return model.encode(df[cleaned_question_col].tolist())

# Compute embeddings for each dataset
embeddings_list = [get_embeddings(df) for df in dfs]

# Compute average category embeddings
def average_embeddings_by_category(df):
    category_embeddings = {}
    for category in df[category_col].dropna().unique():
        category_questions = df[df[category_col] == category][cleaned_question_col].tolist()
        if category_questions:
            category_embeddings[category] = model.encode(category_questions).mean(axis=0)
    return category_embeddings

# Compute category embeddings for each dataset
category_embeddings_list = [average_embeddings_by_category(df) for df in dfs]

# Compute cosine similarities between matching categories
similarities = []
for i, cat_emb_1 in enumerate(category_embeddings_list):
    for j, cat_emb_2 in enumerate(category_embeddings_list):
        if i < j:
            for category, embedding_1 in cat_emb_1.items():
                if category in cat_emb_2:
                    embedding_2 = cat_emb_2[category]
                    similarity = cosine_similarity(embedding_1.reshape(1, -1), embedding_2.reshape(1, -1))[0][0]
                    similarities.append({
                        'Chatbot 1': chatbot_names[i],  # Use chatbot name
                        'Chatbot 2': chatbot_names[j],  # Use chatbot name
                        'Category': category,
                        'Cosine Similarity': similarity
                    })

# Convert results to DataFrame and save
similarities_df = pd.DataFrame(similarities)
similarities_df.to_csv('category_similarities.csv', index=False)

# Print sample results
print(similarities_df.head())
