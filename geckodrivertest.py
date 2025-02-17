from selenium import webdriver
from selenium.webdriver.firefox.service import Service

# Create WebDriver for Firefox
service = Service("/opt/homebrew/bin/geckodriver")  # Adjust if needed
driver = webdriver.Firefox(service=service)

# Open a website
driver.get("https://www.mozilla.org")

# Close browser
driver.quit()
