import pandas as pd
import matplotlib.pyplot as plt

# List of CSV file paths and corresponding chatbot names
csv_files = [
    ('yeti/yeti_responses.csv', 'YETI'),
    ('fi/fi_responses.csv', 'Fi GPS'),
    ('rufus/rufus_responses.csv', 'Rufus')
]

# Function to calculate the average response length
def calculate_average_length(csv_file):
    df = pd.read_csv(csv_file)
    df['response_length'] = df['full_response'].apply(len)
    return df['response_length'].mean()

# List to store results
chatbot_names = []
average_lengths = []

# Loop through the CSV files and calculate the average length for each
for file, chatbot in csv_files:
    avg_length = calculate_average_length(file)
    chatbot_names.append(chatbot)
    average_lengths.append(avg_length)

# Create a bar graph to compare the average response lengths
plt.figure(figsize=(10, 6))
plt.bar(chatbot_names, average_lengths, color=['#F4D03F', '#2E86C1', '#58D68D'])
plt.xlabel('Chatbot')
plt.ylabel('Average Response Length (characters)')
plt.title('Average Response Length Comparison by Chatbot')
plt.show()
