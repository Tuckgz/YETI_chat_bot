import pandas as pd
import re
import textstat
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# AI-like phrases (expandable)
ai_phrases = [
    "I'm sorry, but I can't", "As an AI language model", "I don't have personal opinions",
    "However, I can provide", "Let me know if you need more information"
]

def analyze_response(text):
    if not isinstance(text, str) or text.strip() == "":
        return 0  # Empty or invalid response
    
    words = text.split()
    num_words = len(words)
    num_unique_words = len(set(words))
    lexical_diversity = num_unique_words / num_words if num_words else 0
    
    sentences = re.split(r'[.!?]', text)
    avg_sentence_length = sum(len(s.split()) for s in sentences if s.strip()) / len(sentences) if sentences else 0
    
    sentiment = SentimentIntensityAnalyzer().polarity_scores(text)
    sentiment_score = sentiment['compound']  # Close to 0 is more AI-like
    
    ai_phrase_hits = sum(text.lower().count(phrase.lower()) for phrase in ai_phrases)
    
    # Compute AI-likelihood score (tune weighting as needed)
    ai_likelihood = (
        (1 - lexical_diversity) * 30 + 
        (5 / (1 + avg_sentence_length)) * 20 + 
        (abs(sentiment_score) * -30) +  # Neutral sentiment is more AI-like
        (ai_phrase_hits * 10)
    )
    ai_likelihood = max(0, min(100, ai_likelihood))  # Clamp between 0-100
    
    return round(100 - ai_likelihood, 2)  # Higher score = more human-like

# Load CSV
df = pd.read_csv("filtered_uncertain_responses.csv")
df["Human_AI_Score"] = df["full_response"].apply(analyze_response)

# Save results
df.to_csv("responses_scored.csv", index=False)
print("Analysis complete! Results saved in responses_scored.csv")
