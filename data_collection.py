import cloudscraper
from bs4 import BeautifulSoup
import pandas as pd

# Create a CloudScraper object
scraper = cloudscraper.create_scraper()

# URL of PropertyGuru rental property search for Singapore
search_url = "https://www.propertyguru.com.sg/property-for-rent"

# Create list to store property information
property_list = []

# Create counter for the number of scraped properties
n_scraped = 0

# Loop through the search results pages
for page in range(1, 20):  # range(1, n_pages + 1):
    # Make a search request
    response = scraper.get(search_url + f"/{page}")

    # Parse the search results
    soup = BeautifulSoup(response.content, "lxml")

    # Detect captcha
    if "captcha" in soup.text:
        print("Captcha detected when trying to scrape " + search_url + f"/{page}")

    # Get list of property cards that contain property information (identified by div tags with a specific class)
    property_card_list = soup.find_all("div", {"class": "listing-card"})

    # Loop through the property cards
    for property_card in property_card_list:
        # Get property name (identified by an HTML anchor tag with a specific class and item property)
        name = property_card.find("a", {"class": "nav-link", "itemprop": "url"}).get_text()

        # Get property address (identified by an HTML span tag with a specific item property)
        address = property_card.find("span", {"itemprop": "streetAddress"}).get_text()

        # Get property price (identified by an HTML span tag with a specific class)
        price = property_card.find(class_="price").get_text()

        # Get property size (identified by an HTML list tag with a specific class)
        size = property_card.find("li", {"class": "listing-floorarea"}).get_text()

        # Get bedrooms and bathrooms
        # Get HTML tag that contains the information about the bedrooms and bathrooms
        rooms_tag = property_card.find("li", {"class": "listing-rooms"})
        # If the HTML tag is missing, set bedrooms and bathrooms as missing values
        if rooms_tag is None:
            bedrooms = ""
            bathrooms = ""
        # If the property is identified as a room in a shared flat, assign bedrooms as "Room" and bathrooms as missing
        elif "Room" in rooms_tag.get_text():
            bedrooms = "Room"
            bathrooms = ""
        # If the property is identified as a studio, assign bedrooms as "Studio" and bathrooms as missing
        elif "Studio" in rooms_tag.get_text():
            bedrooms = "Studio"
            bathrooms = ""
        # If the property is not a room or a studio, extract the bedrooms and bathrooms information
        else:
            bedrooms = rooms_tag.find(class_="bed").get_text(strip=True) if rooms_tag.find(class_="bed") is not None else ""
            bathrooms = rooms_tag.find(class_="bath").get_text(strip=True) if rooms_tag.find(class_="bath") is not None else ""

        # Get property type, furnishing, and build year (identified by an HTML unordered list tag with a specific class)
        property_type_furnishing_year = soup.find("ul", {"class": "listing-property-type"}).get_text()

        # Get distance to MRT (identified by an HTML unordered list tag with a specific data-automation-id)
        mrt_distance_tag = property_card.find("ul", {"data-automation-id": "listing-features-walk"})
        # If the HTML tag is missing, assign a missing value
        if mrt_distance_tag is None:
            mrt_distance = ""
        # If the HTML tag is present, extract the MRT distance information
        else:
            mrt_distance = mrt_distance_tag.get_text(strip=True)

        # Get property agent description (identified by an HTML div tag with a specific class)
        agent_description = property_card.find("div", {"class": "featured-description"}).get_text().split('"')[1]

        # Add property to the property list
        property_list.append([name, address, price, size, bedrooms, bathrooms, property_type_furnishing_year,
                              mrt_distance, agent_description])

    # Update the number of scraped properties
    n_scraped += len(property_card_list)
    # Show number of scraped properties
    print(f"Number of scraped properties: {n_scraped}")

# Show first 10 elements of the list of properties
print(property_list[:10])

# Show total number of properties
print(len(property_list))

# Convert list of properties to pandas dataframe
new_data = pd.DataFrame(property_list, columns=["name", "address", "price", "size", "bedrooms", "bathrooms",
                                                "property_type_furnishing_year", "mrt_distance", "agent_description"])

# Read the existing csv
df = pd.read_csv("data/rental_prices_singapore.csv")

# Append the new data to the existing dataframe
df = pd.concat([df, new_data], ignore_index=True)

# Save dataframe as csv
df.to_csv("data/rental_prices_singapore.csv", index=False)
