import pandas as pd

# Define the files and their labels
csv_files = {
    "yeti_responses.csv": "yeti",
    "rufus_responses.csv": "rufus",
    "fi_responses.csv": "fi"
}

# Define reset conditions (values in the first column that indicate a new batch)
reset_values = {
    "What proof do I need to submit a YETI warranty claim?", 
    "You said the YETI Rambler is durable—how does it compare to competitors",
    "Does YETI make a solar-powered cooler?",
    "Is the Kindle Oasis currently in stock?",
    "What Amazon smart home devices come in black? Do they have a matte finish?",
    "Does Amazon allow order cancellations before shipping?",
    "You said the Fi Collar can be tracked in real-time—how often does it update?"
    }

all_data = []

for file, label in csv_files.items():
    df = pd.read_csv(file)  # Read CSV
    last_two_columns = df.iloc[:, -2:].copy()  # Extract last two columns

    # Get first column
    first_column = df.iloc[:, 0]

    # Initialize query_num and list to store values
    query_nums = []
    query_num = 1  # Start query numbering from 1

    for value in first_column:
        if value in reset_values:  # If the value matches a reset condition
            query_num = 1  # Increment query number
        query_nums.append(query_num)
        query_num += 1

    last_two_columns.insert(0, "chat_bot", label)
    last_two_columns.insert(1, "query_num", query_nums)

    all_data.append(last_two_columns)  # Store processed DataFrame

    print(f"Processed {file} with label {label}:")
    print(last_two_columns.head(), "\n")

# Combine all processed data
combined_df = pd.concat(all_data, ignore_index=True)

# Save to a new CSV file
combined_df.to_csv("timing_data.csv", index=False)
print("Saved timing data to timing_data.csv")
