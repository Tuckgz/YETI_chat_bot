import pickle
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import os

# Set up the WebDriver
service = Service("/opt/homebrew/bin/geckodriver")  # Update with your GeckoDriver path
driver = webdriver.Firefox(service=service)

# Flag to control whether to append to the existing CSV or overwrite
append_to_csv = True  # Change to False to overwrite the CSV

# Initialize an empty list to store data
data = []

try:
    # Load the questions from the CSV
    questions_df = pd.read_csv("fi_gps_questions.csv")
    
    # Navigate to the website
    driver.get("https://tryfi.com/")

    # Wait for the page to load
    time.sleep(5)

    # Ensure iframes are present
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "iframe")))
    iframes = driver.find_elements(By.TAG_NAME, "iframe")

    # Switch to the chatbot's iframe
    driver.switch_to.frame(iframes[1])

    # Locate the chat input field
    chat_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "expandable-input-chat-input"))
    )

    # Loop through each question in the CSV
    for _, row in questions_df.iterrows():
        question = row["Question"]

        # Count the number of responses before submitting the question
        initial_responses = len(driver.find_elements(By.CSS_SELECTOR, "[data-testid='widget-chat-bubble-text']"))
        print("Initial response count:",initial_responses)
        # Send the question
        chat_input.send_keys(question)
        chat_input.send_keys(Keys.RETURN)

        # Start timing the partial response
        start_time = time.time()

        # Wait until a new response appears (ensures we don't submit too quickly)
        WebDriverWait(driver, 30).until(
            lambda d: len(d.find_elements(By.CSS_SELECTOR, "[data-testid='widget-chat-bubble-text']")) > initial_responses+1
        )

        response_time = time.time() - start_time  # Partial response time

        # Capture only the last chatbot response
        key_elements = driver.find_elements(By.CSS_SELECTOR, "[data-testid='widget-chat-bubble-text']")
        last_bot_response = key_elements[-1].text if key_elements else "No response captured"

        # Append the data
        data.append({
            "question": question,
            "full_response": last_bot_response.strip(),
            "partial_response_time": response_time,
            "total_response_time": response_time
        })

        # Print the results
        print("fi Response:", last_bot_response.strip())
        print(f"Total Response Time: {response_time:.2f} seconds")

except Exception as e:
    print("An error occurred:", e)

finally:
    # Close the browser
    driver.quit()

    # Convert the data to a pandas DataFrame
    df = pd.DataFrame(data)

    # Save or append to CSV
    if append_to_csv and os.path.exists("fi_responses.csv"):
        df.to_csv("fi_responses.csv", mode="a", header=False, index=False)
        print("Data appended to fi_responses.csv")
    else:
        df.to_csv("fi_responses.csv", index=False)
        print("Data saved to fi_responses.csv")
