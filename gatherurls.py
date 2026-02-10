import requests
from bs4 import BeautifulSoup

def getSupplements(url):

    # Send a GET request to the webpage
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
    # Parse the webpage content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the desired content (e.g., all paragraph tags)
        paragraphs = soup.find_all('p')

        # Print the text of each paragraph
        for paragraph in paragraphs:
            print(paragraph.get_text())
    else:
        print('Failed to retrieve webpage')

#print(getSupplements(new_url))

def get_gnc_listing_urls(keyphrase, num_pages=1):
    base_url = "https://www.gnc.com/search?q="
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    urls = []

    for page in range(1, num_pages + 1):
        search_url = f"{base_url}{keyphrase}&page={page}"
        response = requests.get(search_url, headers=headers)
        
        # Debug print for response status
        print(f"Page {page} Response Status: {response.status_code}")
        
        if response.status_code != 200:
            print("Failed to retrieve the page. Exiting.")
            return urls

        soup = BeautifulSoup(response.content, "html.parser")
        
        # Debug print for HTML content
        print(response.text[:1000])  # Print the first 1000 characters of the HTML

        # Adjust the selector based on the structure of GNC's search result page
        search_results = soup.find_all("a", {"class": "product-title-link"})
        
        # Debug print for number of found elements
        print(f"Number of search results found: {len(search_results)}")
        
        for result in search_results:
            url = "https://www.gnc.com" + result["href"]
            urls.append(url)

    return urls

# Example usage
keyphrase = "gym supplements"
num_pages = 3
urls = get_gnc_listing_urls(keyphrase, num_pages)
for url in urls:
    print(url)

for url in urls:
    print("hello")
    print(getSupplements(url))



#Populate urls into the database
import mysql.connector
from mysql.connector import Error

# MySQL database connection
def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="your_username",  # Replace with your MySQL username
            password="your_password",  # Replace with your MySQL password
            database="your_database"  # Replace with your database name
        )
        if connection.is_connected():
            print("Connection successful!")
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# Create table to store URLs
def create_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS supplements (
                id INT AUTO_INCREMENT PRIMARY KEY,
                url TEXT NOT NULL
            );
        """)
        print("Table `supplements` is ready.")
    except Error as e:
        print(f"Error creating table: {e}")

# Insert URLs into the table
def insert_urls(connection, urls):
    try:
        cursor = connection.cursor()
        for url in urls:
            cursor.execute("INSERT INTO supplements (url) VALUES (%s)", (url,))
        connection.commit()
        print(f"{len(urls)} URLs inserted into the database.")
    except Error as e:
        print(f"Error inserting URLs: {e}")

# Main program
if __name__ == "__main__":
    # Replace this with your actual GNC scraper function
    def get_gnc_listing_urls():
        # Mock data for demonstration. Replace with the actual scraper function output.
        return [
            "https://www.gnc.com/supplement1",
            "https://www.gnc.com/supplement2",
            "https://www.gnc.com/supplement3"
        ]

    # Retrieve URLs
    urls = get_gnc_listing_urls()
    print("Scraped URLs:", urls)

    # Database operations
    db_connection = create_connection()
    if db_connection:
        create_table(db_connection)
        insert_urls(db_connection, urls)
        db_connection.close()

