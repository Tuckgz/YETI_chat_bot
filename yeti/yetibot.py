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

def get_message_list_size():
    message_list_log = driver.find_element(By.ID, 'MESSAGE_LIST_LOG')
    # print(len(message_list_log.find_elements(By.CSS_SELECTOR, '*')))
    return len(message_list_log.find_elements(By.CSS_SELECTOR, '*'))

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
    driver.get("https://www.yeti.com")
    
    # Load cookies from file
    load_cookies(driver, "yeti/yeti_cookies.pkl")
    
    # Reload the page after adding cookies
    driver.refresh()
    
    # Wait for the page to load
    time.sleep(5)

    # # Locate the Yeti button by its ID
    # yeti_button = driver.find_element(By.ID, 'ada-chat-button')
    # ActionChains(driver).move_to_element(yeti_button).click().perform()
    # time.sleep(5)
    iframe_button = driver.find_element(By.ID, "ada-button-frame")
    driver.switch_to.frame(iframe_button)

    # Step 2: Find and click the ada-chat-button
    chat_button = driver.find_element(By.ID, "ada-chat-button")
    chat_button.click()
    driver.switch_to.default_content()
    time.sleep(5)  # Wait for the chat window to open (adjust if necessary)

    # Step 3: Switch to the iframe containing the chat input (ada-chat-frame)
    
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "iframe")))

    # Now, let's check again how many iframes are available
    iframes = driver.find_elements(By.TAG_NAME, "iframe")
    print(f"Found {len(iframes)} iframes.")

    if len(iframes) > 0:
        # Print all iframe src attributes (or other useful info) to debug
        for index, iframe in enumerate(iframes):
            print(f"Iframe {index}: {iframe.get_attribute('src')}")
    else:
        print("No iframes found on the page.")
    
    driver.switch_to.frame(iframes[5])
    # Loop through each question in the CSV
    for _, row in questions_df.iterrows():
        question = row['Question']
        
        # Find the text area by its ID and send keys
        chat_input = driver.find_element(By.CSS_SELECTOR, "[data-testid='MessageInput']")
        chat_input.send_keys(question)
        chat_input.send_keys(Keys.RETURN)
        
        # Start timing the partial response (for the first element)
        start_time = time.time()
        previous_size = get_message_list_size()
        print(previous_size)
        counter = 0
        cascade = 0
        prev_time = start_time
        part_time = None

        while counter < 50:
            current_size = get_message_list_size()
            if current_size != previous_size:
                print(current_size)
                previous_size = current_size
                if part_time is None and prev_time - time.time() < 0.25 and prev_time != start_time:
                    cascade += 1
                    if cascade > 3:
                        print("setting part time")
                        part_time = time.time()
                prev_time = time.time()
            elif part_time is not None:
                counter += 1
        
            time.sleep(0.1)

        partial_response_time = part_time - start_time
        end_time = prev_time - start_time

        time.sleep(2)
        # Capture the full response after thumbs up appears
        key_elements = driver.find_elements(By.CSS_SELECTOR, '[data-testid="MessageGroupNewBot"]')

        if key_elements:
            full_response = key_elements[-1].text  # Get only the last message
        else:
            full_response = ""  # Handle cases where no messages are found


        # Append the data to the list
        data.append({
            "question": question,
            "full_response": full_response.strip(),
            "partial_response_time": partial_response_time,
            "total_response_time": end_time
        })

        # Print the results
        print("Yeti Response:", full_response.strip())
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
    if append_to_csv and os.path.exists("yeti/yeti_general_responses.csv"):
        # Append the data to the existing CSV
        df.to_csv("yeti/yeti_general_responses.csv", mode='a', header=False, index=False)
        print("Data appended to yeti_general_responses.csv")
    else:
        # Overwrite the existing CSV or create a new one
        df.to_csv("yeti/yeti_general_responses.csv", index=False)
        print("Data saved to yeti_general_responses.csv")
