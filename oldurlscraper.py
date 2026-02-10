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


