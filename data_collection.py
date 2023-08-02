import cloudscraper
from bs4 import BeautifulSoup
import pandas as pd

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

# List of properties
property_list = []

# Counter for the number of scraped properties
n_scraped = 0

# Iterate all pages
for page in range(1, 6):  # n_pages + 1
    # Make a search request
    response = scraper.get(search_url + f"/{page}")
    # Parse the search results
    soup = BeautifulSoup(response.content, "lxml")

    # Get list of property cards that contain property information (identified by div tags with a specific class)
    property_card_tags = soup.find_all("div", {"class": "listing-card"})

    # Iterate all property cards
    for property_card in property_card_tags:
        # Get property name (identified by an HTML anchor tag with a specific class and item property)
        name = property_card.find("a", {"class": "nav-link", "itemprop": "url"}).get_text()

        # Get property address (identified by an HTML span tag with a specific item property)
        address = property_card.find("span", {"itemprop": "streetAddress"}).get_text()

        # Get property price (identified by an HTML span tag with a specific class)
        price = property_card.find(class_="price").get_text()

        # Get property size (identified by an HTML list tag with a specific class)
        size = property_card.find("li", {"class": "listing-floorarea"}).get_text()

        # Get bedrooms and bathrooms (identified by an HTML list tag with a specific class)
        rooms_tag = property_card.find("li", {"class": "listing-rooms"})
        if rooms_tag is None:
            bedrooms = ""
            bathrooms = ""
        elif "Room" in rooms_tag.get_text():
            bedrooms = "Room"
            bathrooms = ""
        elif "Studio" in rooms_tag.get_text():
            bedrooms = "Studio"
            bathrooms = ""
        else:
            bedrooms = rooms_tag.find(class_="bed").get_text(strip=True)
            bathrooms = rooms_tag.find(class_="bath").get_text(strip=True)

        # Get property type, furnishing, and build year (identified by an HTML unordered list tag with a specific class)
        property_type_furnishing_year = soup.find("ul", {"class": "listing-property-type"}).get_text()

        # Get distance to MRT (identified by an HTML unordered list tag with a specific data-automation-id)
        mrt_distance_tag = property_card.find("ul", {"data-automation-id": "listing-features-walk"})
        if mrt_distance_tag is None:
            mrt_distance = ""
        else:
            mrt_distance = mrt_distance_tag.get_text(strip=True)

        # Get property agent description (identified by an HTML div tag with a specific class)
        agent_description = property_card.find("div", {"class": "featured-description"}).get_text().split('"')[1]

        # Add property to the list
        property_list.append([name, address, price, size, bedrooms, bathrooms, property_type_furnishing_year,
                              mrt_distance, agent_description])

    # Update the number of scraped properties
    n_scraped += len(property_card_tags)
    # Show number of scraped properties
    print(f"Number of scraped properties: {n_scraped}")

# Show list of properties
print(property_list[:10])
print(len(property_list))

# Convert list of properties to pandas dataframe
df = pd.DataFrame(property_list, columns=["name", "address", "price", "size", "bedrooms", "bathrooms",
                                          "property_type_furnishing_year", "mrt_distance", "agent_description"])

# Save dataframe to csv
df.to_csv("data/rental_prices_singapore.csv", index=False)
