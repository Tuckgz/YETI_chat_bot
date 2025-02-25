import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Updated file paths
file_paths = {
    "YETI Specific": 'yeti/yeti_responses.csv',
    "YETI General": 'yeti/yeti_general_responses.csv',
    "Rufus Specific": 'rufus/rufus_responses.csv',
    "Rufus General": 'rufus/rufus_general_responses.csv',
    "Fi Specific": 'fi/fi_responses.csv',
    "Fi General": 'fi/fi_general_responses.csv'
}

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

# Dictionary to store average intensity values
company_averages = {}

# Process multiple CSVs and calculate averages
for name, file_path in file_paths.items():
    df = load_data(file_path)
    df = analyze_sentiment_intensity(df, file_path)
    
    # Save the results to a CSV file
    output_file = f'sentiment_intensity_{file_path.replace("/", "_")}'
    df.to_csv(output_file, index=False)
    
    # Extract company name (e.g., "Yeti", "Rufus", "Fi")
    company_name = name.split()[0]
    
    # Store average intensity for this dataset
    avg_intensity = df['Emotion Intensity'].mean()
    
    # Add to combined averages
    if company_name not in company_averages:
        company_averages[company_name] = []
    company_averages[company_name].append(avg_intensity)

# Compute final company averages
final_averages = {company: np.mean(intensities) for company, intensities in company_averages.items()}

# Plot the company-wide average emotion intensities
plt.figure(figsize=(8, 5))
plt.bar(final_averages.keys(), final_averages.values(), color=['blue', 'orange', 'green'])
plt.xlabel('Company')
plt.ylabel('Average Emotion Intensity')
plt.title('Combined Emotion Intensity Averages per Company')
plt.ylim(0, 1)  # Emotion intensity is between 0 and 1
plt.show()
