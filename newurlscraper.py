from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialize the WebDriver
service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode for automation
driver = webdriver.Chrome(service=service, options=options)

# Define the search URL and parameters
search_url = "https://www.gnc.com/search?q=gym+supplements&lang=default"  # Replace with your search query
driver.get(search_url)

# Wait for the search results to load
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "thumb-link")))

# Extract product URLs
product_elements = driver.find_elements(By.CLASS_NAME, "product-tile__name")
product_links = [element.get_attribute("href") for element in product_elements]

# Print the extracted URLs
for link in product_links:
    print(link)

driver.quit()
