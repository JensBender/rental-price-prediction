import cloudscraper
from bs4 import BeautifulSoup

# Create a CloudScraper object
scraper = cloudscraper.create_scraper()

# URL of PropertyGuru search in Singapore
search_url = "https://www.propertyguru.com.sg/property-for-rent"

# Make a property search request for residential rental properties using the scraper
response = scraper.get(search_url + "?market=residential")

# Parse the search results using Beautiful Soup
soup = BeautifulSoup(response.content, "lxml")

# Get number of properties
# Get HTML tag that contains the number of rental properties (identified by a span tag with a specific class)
n_properties_tag = soup.find("span", {"class": "shorten-search-summary-title"})
# Get number of properties (also remove thousands separator and convert to int)
n_properties = int(n_properties_tag.get_text(strip=True).split(" ")[0].replace(",", ""))
print("Number of properties: ", n_properties)

# Get number of pages with search results
# Get HTML tag that contains the number of results pages (identified by an unordered list tag with a specific class)
n_pages_tag = soup.find("ul", {"class": "pagination"})
# Get number of pages
n_pages = int(n_pages_tag.get_text().split("...")[1].split("»")[0])
print("Number of pages with search results: ", n_pages)

# Counter for the number of scraped properties
n_scraped = 0

# Iterate all pages
for page in range(1, 10):  # n_pages + 1
    # Make a search request
    response = scraper.get(search_url + f"/{page}")
    # Parse the search results
    soup = BeautifulSoup(response.content, "lxml")
    # Get list of property cards that contain property information (identified by div tags with a specific class)
    property_card_tags = soup.find_all("div", {"class": "listing-card"})
    # Update the number of scraped properties
    n_scraped += len(property_card_tags)
    # Show number of scraped properties
    print(f"Number of scraped properties: {n_scraped}")
