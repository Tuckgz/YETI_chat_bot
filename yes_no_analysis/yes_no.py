import csv
import os

# List of modal verbs that typically indicate yes-or-no questions
modal_verbs = {"is", "are", "was", "were", "do", "does", "did", "can", "could", "will", "would", "shall", "should", "may", "might", "must"}

def is_yes_no_question(question):
    """Check if the question is a yes-or-no question by looking for leading modal verbs."""
    first_word = question.strip().split()[0].lower()
    return first_word in modal_verbs

def is_yes_no_response(response):
    """Check if the response starts with 'yes' or 'no'."""
    response_lower = response.strip().lower()
    return response_lower.startswith("yes") or response_lower.startswith("no")

def main(input_csv, output_csv, chatbot_name):
    total_yes_no_questions = 0
    total_yes_no_answers = 0

    with open(input_csv, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row if there is one
        for row in reader:
            question = row[0]  # Explicitly use the first column for the question
            response = row[1]  # Explicitly use the second column for the response

            if is_yes_no_question(question):
                total_yes_no_questions += 1
                if is_yes_no_response(response):
                    total_yes_no_answers += 1

    # Append results to the output CSV file (or create it if it doesn't exist)
    file_exists = os.path.isfile(output_csv)
    with open(output_csv, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write the header only if the file is being created for the first time
        if not file_exists:
            writer.writerow(['chat_bot', 'total_yes_no_questions', 'total_yes_no_answers'])
        # Write the data row
        writer.writerow([chatbot_name, total_yes_no_questions, total_yes_no_answers])

if __name__ == "__main__":
    input_csv = 'yeti/yeti_responses.csv'  # Replace with your input CSV file path
    output_csv = 'yes_no.csv'  # Replace with your desired output CSV file path
    chatbot_name = 'yeti'  # Replace with your chatbot's name
    main(input_csv, output_csv, chatbot_name)