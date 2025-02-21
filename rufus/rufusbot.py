import pickle
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import os

# Set up the WebDriver
service = Service("/opt/homebrew/bin/geckodriver")  # Update with your GeckoDriver path
driver = webdriver.Firefox(service=service)

# Load cookies from pickle file
def load_cookies(driver, cookies_file):
    try:
        with open(cookies_file, "rb") as cookiefile:
            cookies = pickle.load(cookiefile)
            for cookie in cookies:
                driver.add_cookie(cookie)
    except FileNotFoundError:
        print("Cookies file not found. Starting a fresh session.")

# Flag to control whether to append to the existing CSV or overwrite
append_to_csv = True  # Change this to False to overwrite the CSV

# Initialize an empty list to store data
data = []

try:
    # Load the questions from the CSV
    questions_df = pd.read_csv('general_chatbot_questions.csv')
    
    # Navigate to Amazon's homepage
    driver.get("https://www.amazon.com")
    
    # Load cookies from file
    load_cookies(driver, "rufus/amazon_cookies.pkl")
    
    # Reload the page after adding cookies
    driver.refresh()
    
    # Wait for the page to load
    time.sleep(2)

    # Locate the Rufus button by its ID
    rufus_button = driver.find_element(By.ID, "nav-rufus-disco")

    # Click the Rufus button
    ActionChains(driver).move_to_element(rufus_button).click().perform()
    time.sleep(2)  # Wait for the Rufus panel to open

    # Loop through each question in the CSV
    for _, row in questions_df.iterrows():
        question = row['Question']

        # Find the text area by its ID and send keys
        chat_input = driver.find_element(By.ID, "rufus-text-area")
        chat_input.send_keys(question)
        chat_input.send_keys(Keys.RETURN)
        
        # Start timing and track response growth
        start_time = time.time()
        initial_response_count = len(driver.find_elements(By.CSS_SELECTOR, "div.rufus-conversation span"))

        while True:
            key_elements = driver.find_elements(By.CSS_SELECTOR, "div.rufus-conversation span")
            if len(key_elements) > initial_response_count:
                partial_response_time = time.time() - start_time
                partial_index = len(key_elements)
                break

        # Wait for the thumbs-up image to appear (final response indicator)
        try:
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.ID, "rufus-thumbs-up"))
            )
        except Exception as e:
            continue
        end_time = time.time() - start_time

        # Capture responses from the first detected response until the last one
        key_elements = driver.find_elements(By.CSS_SELECTOR, "div.rufus-conversation span")
        full_response = " ".join([key.text for key in key_elements[partial_index - 1:]])

        # Append the data to the list
        data.append({
            "question": question,
            "full_response": full_response.strip(),
            "partial_response_time": partial_response_time,
            "total_response_time": end_time
        })

        # Print the results
        print("Rufus Full Response:", full_response.strip())
        print(f"Partial Response Time (first element): {partial_response_time:.2f} seconds")
        print(f"Total Response Time: {end_time:.2f} seconds")

except Exception as e:
    print("An error occurred:", e)

finally:
    # Close the browser
    driver.quit()

    # Convert the data to a pandas DataFrame
    df = pd.DataFrame(data)

    # Check if the CSV file exists
    if append_to_csv and os.path.exists("rufus_general_responses.csv"):
        # Append the data to the existing CSV
        df.to_csv("rufus_general_responses.csv", mode='a', header=False, index=False)
        print("Data appended to rufus_general_responses.csv")
    else:
        # Overwrite the existing CSV or create a new one
        df.to_csv("rufus_general_responses.csv", index=False)
        print("Data saved to rufus_general_responses.csv")
