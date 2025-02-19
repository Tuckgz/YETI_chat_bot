import csv
import matplotlib.pyplot as plt

# Set a modern font and style
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial']  # Use Arial or another modern font
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['axes.titleweight'] = 'bold'

# Function to create a donut chart for a row
def create_donut_chart(chatbot_name, total_yes_no_questions, total_yes_no_answers, colors):
    labels = ['Yes/No Answers', 'Other Answers']
    sizes = [total_yes_no_answers, total_yes_no_questions - total_yes_no_answers]
    explode = (0, 0)  # No explosion for a cleaner look

    # Create the donut chart with a slightly smaller figure size
    fig, ax = plt.subplots(figsize=(6, 6))  # Adjusted to 6x6 for a more compact size
    wedges, _, autotexts = ax.pie(
        sizes, 
        explode=explode, 
        colors=colors, 
        startangle=140, 
        wedgeprops=dict(width=0.4, edgecolor='w'),  # Create a donut shape
        autopct='%1.1f%%',  # Add percentages to the slices
        pctdistance=0.8,  # Adjust the position of the percentages
        textprops={'fontsize': 12, 'fontweight': 'bold', 'color': 'black'}  # Style the percentages
    )

    # Add a title with a modern font
    ax.set_title(f'Yes-Or-No Responses for {chatbot_name}', fontsize=16, fontweight='bold', pad=20)

    # Add a legend without labels on the chart
    ax.legend(wedges, labels, title="Categories", loc="upper right", bbox_to_anchor=(1, 0, 0.5, 1), fontsize=12)

    # Use a tight layout to avoid overlap
    plt.tight_layout()
    plt.show()

def main(input_csv):
    # Define a cohesive, modern color palette
    colors_list = [
        ['#2E86C1', '#AED6F1'],  # Blue tones
        ['#58D68D', '#ABEBC6'],  # Green tones
        ['#F4D03F', '#FDEBD0']   # Gold tones
    ]

    with open(input_csv, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for i, row in enumerate(reader):
            chatbot_name = row[0]
            total_yes_no_questions = int(row[1])
            total_yes_no_answers = int(row[2])
            create_donut_chart(chatbot_name, total_yes_no_questions, total_yes_no_answers, colors_list[i])

if __name__ == "__main__":
    input_csv = 'yes_no.csv'  # Replace with your input CSV file path
    main(input_csv)