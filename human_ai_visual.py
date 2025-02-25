import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV files
chatbot1_df = pd.read_csv("yeti_responses_scored.csv")
chatbot2_df = pd.read_csv("rufus_responses_scored.csv")
chatbot3_df = pd.read_csv("fi_responses_scored.csv")

# Function to calculate text length (average number of words per response)
def calculate_avg_text_length(df):
    return df["full_response"].apply(lambda x: len(str(x).split())).mean()

# Function to calculate repetition ratio (percentage of repeated words)
def calculate_repetition_ratio(df):
    def repetition_ratio(text):
        words = str(text).split()
        if not words:
            return 0
        unique_words = set(words)
        return 1 - (len(unique_words) / len(words))
    return df["full_response"].apply(repetition_ratio).mean()

# Calculate metrics for each chatbot
metrics = {
    'Chatbot 1': {
        'Human_AI_Score': chatbot1_df["Human_AI_Score"].mean(),
        'Text_Length': calculate_avg_text_length(chatbot1_df),
        'Repetition_Ratio': calculate_repetition_ratio(chatbot1_df)
    },
    'Chatbot 2': {
        'Human_AI_Score': chatbot2_df["Human_AI_Score"].mean(),
        'Text_Length': calculate_avg_text_length(chatbot2_df),
        'Repetition_Ratio': calculate_repetition_ratio(chatbot2_df)
    },
    'Chatbot 3': {
        'Human_AI_Score': chatbot3_df["Human_AI_Score"].mean(),
        'Text_Length': calculate_avg_text_length(chatbot3_df),
        'Repetition_Ratio': calculate_repetition_ratio(chatbot3_df)
    }
}

# Extract data for plotting
chatbots = list(metrics.keys())
human_ai_scores = [metrics[chatbot]['Human_AI_Score'] for chatbot in chatbots]
text_lengths = [metrics[chatbot]['Text_Length'] for chatbot in chatbots]
repetition_ratios = [metrics[chatbot]['Repetition_Ratio'] for chatbot in chatbots]

# Create subplots for the three bar charts
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# Plot 1: Human_AI_Score
axes[0].bar(chatbots, human_ai_scores, color=['blue', 'green', 'red'])
axes[0].set_xlabel('Chatbot')
axes[0].set_ylabel('Average Human_AI_Score')
axes[0].set_title('Human_AI_Score Comparison')
axes[0].set_ylim(0, 100)  # Assuming the score ranges from 0 to 100
for i, score in enumerate(human_ai_scores):
    axes[0].text(i, score + 2, f"{score:.2f}", ha='center')

# Plot 2: Text Length
axes[1].bar(chatbots, text_lengths, color=['blue', 'green', 'red'])
axes[1].set_xlabel('Chatbot')
axes[1].set_ylabel('Average Text Length (Words)')
axes[1].set_title('Text Length Comparison')
for i, length in enumerate(text_lengths):
    axes[1].text(i, length + 2, f"{length:.2f}", ha='center')

# Plot 3: Repetition Ratio
axes[2].bar(chatbots, repetition_ratios, color=['blue', 'green', 'red'])
axes[2].set_xlabel('Chatbot')
axes[2].set_ylabel('Average Repetition Ratio')
axes[2].set_title('Repetition Ratio Comparison')
for i, ratio in enumerate(repetition_ratios):
    axes[2].text(i, ratio + 0.02, f"{ratio:.2f}", ha='center')

# Adjust layout and display
plt.tight_layout()
plt.show()