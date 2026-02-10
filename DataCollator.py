# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from bs4 import BeautifulSoup
# import time

# # Configure Selenium WebDriver
# def setup_driver():
#     options = webdriver.ChromeOptions()
#     options.add_argument("--headless")  # Run in headless mode
#     options.add_argument("--disable-gpu")
#     options.add_argument("--no-sandbox")
#     driver_service = Service("path_to_chromedriver")  # Replace with your ChromeDriver path
#     driver = webdriver.Chrome(service=driver_service, options=options)
#     return driver

# # Scrape data
# def scrape_supplements(driver, url):
#     driver.get(url)
#     try:
#         # Wait for the product listing container to be present
#         wait = WebDriverWait(driver, 10)
#         wait.until(EC.presence_of_element_located((By.CLASS_NAME, "s-main-slot")))

#         soup = BeautifulSoup(driver.page_source, "html.parser")

#         # Extract product titles and ingredients (modify selectors for additional data)
#         products = []
#         product_elements = soup.find_all("div", class_="s-main-slot")
#         for element in product_elements:
#             title = element.find("span", class_="a-size-medium")
#             if title:
#                 title_text = title.text.strip()
#                 products.append({"title": title_text})
#         return products
#     except Exception as e:
#         print(f"Error scraping data: {e}")
#         return []

# # Example usage
# driver = setup_driver()
# url = "https://www.amazon.com/s?k=dietary+supplements"
# products = scrape_supplements(driver, url)
# print(products)
# driver.quit()



# import pandas as pd

# # Load the uploaded CSV files
import pandas as pd

# Initialize empty lists to store dataframes
product_overview_dfs = []
other_ingredients_dfs = []

# List of filenames for product overview and other ingredients
product_overview_files = [
    'ProductOverview_1.csv', 'ProductOverview_2.csv', 'ProductOverview_3.csv', 
    'ProductOverview_4.csv', 'ProductOverview_5.csv', 'ProductOverview_6.csv', 'ProductOverview_7.csv'
]

other_ingredients_files = [
    'OtherIngredients_1.csv', 'OtherIngredients_2.csv', 'OtherIngredients_3.csv',
    'OtherIngredients_4.csv', 'OtherIngredients_5.csv', 'OtherIngredients_6.csv', 'OtherIngredients_7.csv'
]

# Read and store all ProductOverview CSVs
for file in product_overview_files:
    df = pd.read_csv(f'/Users/amystafford/Downloads/DSLD-full-database-CSV/{file}')
    product_overview_dfs.append(df)

# Read and store all OtherIngredients CSVs
for file in other_ingredients_files:
    df = pd.read_csv(f'/Users/amystafford/Downloads/DSLD-full-database-CSV/{file}')
    other_ingredients_dfs.append(df)

# Concatenate all product overview dataframes and reset index
product_overview_df = pd.concat(product_overview_dfs, ignore_index=True)
product_overview_df = product_overview_df[['DSLD ID', 'Serving Size', 'Product Type [LanguaL]']]

# Concatenate all other ingredients dataframes and reset index
other_ingredients_df = pd.concat(other_ingredients_dfs, ignore_index=True)
other_ingredients_df = other_ingredients_df[['DSLD ID', 'Other Ingredients']]

# Merge the datasets on DSLD ID
merged_df = pd.merge(product_overview_df, other_ingredients_df, on='DSLD ID', how='inner')

# Rename columns for clarity
merged_df.rename(columns={
    'Serving Size': 'Serving Size',
    'Product Type [LanguaL]': 'Product Type',
    'Other Ingredients': 'Other Ingredients'
}, inplace=True)

# Remove rows with missing values in any of the relevant columns
cleaned_df = merged_df.dropna(subset=['Serving Size', 'Product Type', 'Other Ingredients'])

# Save the cleaned dataframe to a CSV file
cleaned_df.to_csv('/Users/amystafford/Downloads/cleaned_dietary_supplements.csv', index=False)

# Display the cleaned dataframe
print(cleaned_df.head())
