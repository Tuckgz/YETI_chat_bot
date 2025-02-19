import pandas as pd

# Load the previously generated category similarity CSV
similarities_df = pd.read_csv('category_similarities.csv')

# Ensure necessary columns exist
required_columns = ['Chatbot 1', 'Chatbot 2', 'Category', 'Cosine Similarity']
if not all(col in similarities_df.columns for col in required_columns):
    raise ValueError(f"CSV must contain the following columns: {', '.join(required_columns)}")

# Calculate category similarity score for each category
category_scores = similarities_df.groupby('Category')['Cosine Similarity'].mean().reset_index()
category_scores.rename(columns={'Cosine Similarity': 'Category Similarity Score'}, inplace=True)

# Calculate total similarity score
total_similarity = similarities_df['Cosine Similarity'].mean()

# Add the total similarity score as a row with the category 'Total Similarity'
total_similarity_row = pd.DataFrame([{
    'Category': 'Total Similarity',
    'Category Similarity Score': total_similarity
}])

# Append the total similarity row to the category scores
category_scores = pd.concat([category_scores, total_similarity_row], ignore_index=True)

# Save the results to a new CSV
category_scores.to_csv('category_and_total_similarity_scores.csv', index=False)

# Print out the results
print("Category Similarity Scores for each category:")
print(category_scores)

# Optionally, print out the total similarity score
print("\nTotal Similarity Score (average of all categories):")
print(total_similarity)
