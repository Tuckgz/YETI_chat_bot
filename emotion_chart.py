import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Updated file paths
file1 = 'yeti/yeti_responses.csv'
file2 = 'yeti/yeti_general_responses.csv'
file3 = 'rufus/rufus_responses.csv'
file4 = 'rufus/rufus_general_responses.csv'
file5 = 'fi/fi_responses.csv'
file6 = 'fi/fi_general_responses.csv'

# Initialize VADER Sentiment Analyzer
analyzer = SentimentIntensityAnalyzer()

# Load the CSV file
def load_data(file_path):
    return pd.read_csv(file_path)

# Analyze sentiment intensity using VADER
def analyze_sentiment_intensity(df, file_path):
    emotion_scores = []
    is_yeti = "yeti" in file_path  # Check if the response belongs to Yeti
    adjustment_factor = 0.8 if is_yeti else 1.0  # Reduce impact for Yeti
    
    for response in df['full_response'].astype(str):
        sentiment_scores = analyzer.polarity_scores(response)
        intensity = abs(sentiment_scores['compound']) * adjustment_factor  # Use compound score for intensity
        emotion_scores.append(min(intensity, 1.0))  # Cap intensity at 1.0
    
    df['Emotion Intensity'] = emotion_scores
    return df

# Plot emotion intensity distribution
def plot_emotion_intensity(df, title):
    intensity_bins = {
        "0.0-0.2": len(df[(df['Emotion Intensity'] >= 0.0) & (df['Emotion Intensity'] < 0.2)]),
        "0.2-0.4": len(df[(df['Emotion Intensity'] >= 0.2) & (df['Emotion Intensity'] < 0.4)]),
        "0.4-0.6": len(df[(df['Emotion Intensity'] >= 0.4) & (df['Emotion Intensity'] < 0.6)]),
        "0.6-0.8": len(df[(df['Emotion Intensity'] >= 0.6) & (df['Emotion Intensity'] < 0.8)]),
        "0.8-1.0": len(df[(df['Emotion Intensity'] >= 0.8) & (df['Emotion Intensity'] <= 1.0)])
    }
    
    labels = list(intensity_bins.keys())
    values = list(intensity_bins.values())
    
    # Bar Chart
    plt.figure(figsize=(8, 5))
    plt.bar(labels, [v / len(df) * 100 for v in values])
    plt.xlabel('Emotion Intensity Range')
    plt.ylabel('Percentage of Responses')
    plt.title(f'Emotion Intensity Distribution - {title}')
    plt.show()

# Process multiple CSVs
for file_path in [file1, file2, file3, file4, file5, file6]:
    df = load_data(file_path)
    df = analyze_sentiment_intensity(df, file_path)
    
    # Save the results to a CSV file
    output_file = f'sentiment_intensity_{file_path.replace("/", "_")}'
    df.to_csv(output_file, index=False)
    print(f'Results saved to {output_file}')
    
    # Plot results
    plot_emotion_intensity(df, "Yeti Specific" if "yeti_responses.csv" in file_path else "Yeti General" if "yeti_general_responses.csv" in file_path else "Rufus Specific" if "rufus_responses.csv" in file_path else "Rufus General" if "rufus_general_responses.csv" in file_path else "Fi Specific" if "fi_responses.csv" in file_path else "Fi General")
