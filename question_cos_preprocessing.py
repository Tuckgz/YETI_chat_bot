import pandas as pd
import nltk
import string
import re

# Ensure stopwords are available
try:
    from nltk.corpus import stopwords
    stop_words = set(stopwords.words('english'))
except:
    nltk.download('stopwords')
    from nltk.corpus import stopwords
    stop_words = set(stopwords.words('english'))

# Load ignored words from CSV
def load_ignored_words(csv_path):
    """Load ignored words and their substitutes from a CSV file."""
    df = pd.read_csv(csv_path)
    ignored_words = {}
    for index, row in df.iterrows():
        ignored_words[row['Term'].lower()] = row['Type']
    return ignored_words

# Load CSV files
file_paths = ['yeti/yeti_extra_questions.csv', 'rufus/rufus_extra_questions.csv', 'fi/fi_gps_questions.csv']
ignored_words_csv = 'question_filter_terms.csv'

# Load ignored words from the CSV file
ignored_words = load_ignored_words(ignored_words_csv)

def preprocess_text(text):
    """Lowercase, remove punctuation, stopwords, and specific ignored words, replacing with substitutes."""
    text = str(text).lower()
    text = text.translate(str.maketrans("", "", string.punctuation))

    # First replace multi-word phrases
    for phrase, substitute in ignored_words.items():
        phrase_pattern = r'\b' + re.escape(phrase.lower()) + r'\b'  # Handle case-insensitive replacement
        text = re.sub(phrase_pattern, substitute, text)

    # Then replace individual words
    for word, substitute in ignored_words.items():
        if len(word.split()) == 1:  # Only replace single words (not multi-word phrases)
            word_pattern = r'\b' + re.escape(word.lower()) + r'\b'  # Handle case-insensitive replacement
            text = re.sub(word_pattern, substitute, text)

    text_tokens = text.split()
    text_tokens = [word for word in text_tokens if word not in stop_words]
    
    return " ".join(text_tokens)

# Rerun preprocessing if necessary
def rerun_preprocessing(df, question_col):
    """Reapply preprocessing to check for missed terms."""
    df['cleaned_question'] = df[question_col].apply(preprocess_text)
    return df

# Apply and save the cleaned data
for file_path in file_paths:
    df = pd.read_csv(file_path)
    category_col, question_col = df.columns[:2]  # First column is Category, second is Question
    df = rerun_preprocessing(df, question_col)  # Rerun preprocessing
    cleaned_file_path = file_path.replace(".csv", "_cleaned.csv")
    df.to_csv(cleaned_file_path, index=False)
    print(f"Saved cleaned file: {cleaned_file_path}")
