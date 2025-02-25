from transformers import pipeline
import pandas as pd
import matplotlib.pyplot as plt

# Set a modern font and style
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial']  # Use Arial or another modern font
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['axes.titleweight'] = 'bold'

# Load a pre-trained sentiment or stance detection model (explicitly specify the model)
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Define possible labels for uncertainty or evasion detection
labels = ["certain", "uncertain", "evasive"]

# Function to classify responses based on uncertainty
def classify_uncertainty(response):
    result = classifier(response, candidate_labels=labels)
    # If the model predicts "uncertain" or "evasive" with high confidence
    if result['labels'][0] in ["uncertain", "evasive"] and result['scores'][0] > 0.7:
        return "uncertain/evasive"
    return "certain"

# Function to create a donut chart for a row
def create_donut_chart(total_uncertain, total_responses, colors):
    labels = ['Certain', 'Uncertain/Evasive']
    sizes = [total_responses - total_uncertain, total_uncertain]
    explode = (0, 0)  # No explosion for a cleaner look

    # Create the donut chart
    fig, ax = plt.subplots(figsize=(6, 6))
    wedges, _, autotexts = ax.pie(
        sizes, 
        explode=explode, 
        colors=colors, 
        startangle=140, 
        wedgeprops=dict(width=0.4, edgecolor='w'),
        autopct='%1.1f%%',  # Add percentages to the slices
        pctdistance=0.8,  # Adjust the position of the percentages
        textprops={'fontsize': 12, 'fontweight': 'bold', 'color': 'black'}
    )

    # Add a title with a modern font
    ax.set_title(f"Uncertainty in Yeti Responses\n(General)", fontsize=18, fontweight='bold', pad=20)

    # Add a legend without labels on the chart
    ax.legend(wedges, labels, title="Categories", loc="upper right", bbox_to_anchor=(1, 0, 0.5, 1), fontsize=12)

    # Use a tight layout to avoid overlap
    plt.tight_layout()
    plt.show()

# Read the CSV file (replace 'responses.csv' with your file)
df = pd.read_csv('yeti/yeti_general_responses.csv')

# Assuming the second column contains the responses (replace 'column_name' with the actual name of the column)
df['uncertainty_category'] = df.iloc[:, 1].apply(classify_uncertainty)  # Explicitly referencing the second column

# Count occurrences of each uncertainty category
category_counts = df['uncertainty_category'].value_counts()

# Define a cohesive, modern color palette
# colors_list = ['#AED6F1', '#2E86C1']  # Blue tones
# Uncomment and modify these for different color schemes
# colors_list = ['#ABEBC6', '#58D68D']  # Green tones
colors_list = ['#FDEBD0', '#F4D03F']  # Gold tones

# Create donut chart with counts of uncertain responses
create_donut_chart(category_counts.get("uncertain/evasive", 0), len(df), colors_list)
