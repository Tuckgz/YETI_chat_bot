from transformers import pipeline
import pandas as pd

# Load zero-shot classification model for uncertainty detection
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Define possible labels for uncertainty or evasion detection
labels = ["certain", "uncertain", "evasive"]

# Function to classify responses based on uncertainty
def classify_uncertainty(response):
    result = classifier(response, candidate_labels=labels)
    if result['labels'][0] in ["uncertain", "evasive"] and result['scores'][0] > 0.7:
        return "uncertain/evasive"
    return "certain"

# Function to analyze text repetition, complexity, and structure
def analyze_response(response):
    words = response.split()
    unique_words = set(words)
    
    repetition_ratio = (len(words) - len(unique_words)) / len(words) if len(words) > 0 else 0
    text_length = len(response)
    
    return {
        "text_length": text_length,
        "repetition_ratio": repetition_ratio
    }

# Read the CSV file
df = pd.read_csv('yeti/yeti_responses.csv')

# Classify each response for uncertainty/evasion
df['uncertainty_category'] = df.iloc[:, 1].apply(classify_uncertainty)

# Filter to only "uncertain/evasive" responses
df_filtered = df[df['uncertainty_category'] == "uncertain/evasive"].copy()

# Apply deeper text analysis
df_filtered[['text_length', 'repetition_ratio']] = df_filtered.iloc[:, 1].apply(lambda x: pd.Series(analyze_response(x)))

# Save the filtered responses with analysis
df_filtered.to_csv('filtered_uncertain_responses.csv', index=False)

print("Filtered responses with text analysis saved to 'filtered_uncertain_responses.csv'.")
