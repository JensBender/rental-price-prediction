import cloudscraper
from bs4 import BeautifulSoup

# Create a CloudScraper object
scraper = cloudscraper.create_scraper()

# URL of PropertyGuru search results for residential rental properties in Singapore
search_url = "https://www.propertyguru.com.sg/property-for-rent?market=residential"

# Make a property search request using the scraper
response = scraper.get(search_url)

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

# Iterate all pages
for i in range(n_pages):
    pass

# Get property names
# Get list of all HTML tags that contain names (identified by anchor tags with a specific class and item property)
names_tags = soup.find_all("a", {"class": "nav-link", "itemprop": "url"})
# Get list of names
names_list = [tag.get_text() for tag in names_tags]
print("Names: \n", names_list)

# Get property addresses
# Get list of all HTML tags that contain addresses (identified by span tags with a specific item property)
addresses_tags = soup.find_all("span", {"itemprop": "streetAddress"})
# Get list of addresses
addresses_list = [tag.get_text() for tag in addresses_tags]
print("Addresses: \n", addresses_tags)

# Get property prices
# Get list of all HTML tags that contain the property prices (identified by span tags with a specific class)
prices_tags = soup.find_all(class_="price")
# Get list of prices
prices_list = [tag.get_text() for tag in prices_tags]
print("Prices: \n", prices_list)

# Get property sizes
# Get list of all HTML tags that contain the property sizes in sqft (identified by list tags with a specific class)
sizes_tags = soup.find_all("li", {"class": "listing-floorarea"})
# Keep only tags with sqft-information to remove irrelevant tags with psf-information
sizes_tags = [tag for tag in sizes_tags if "sqft" in tag.get_text()]
# Get list of sizes
sizes_list = [tag.get_text() for tag in sizes_tags]
print("Sizes: \n", sizes_list)

# Get bedrooms and bathrooms
# Get list of all HTML tags that contain the bedrooms and bathrooms (identified by list tags with a specific class)
rooms_tags = soup.find_all("li", {"class": "listing-rooms"})
# Get list of bedrooms and list of bathrooms
bedrooms_list = []
bathrooms_list = []
for tag in rooms_tags:
    if "Room" in tag.get_text():
        bedrooms_list.append("Room")
        bathrooms_list.append(None)
    elif "Studio" in tag.get_text():
        bedrooms_list.append("Studio")
        bathrooms_list.append(None)
    else:
        bedrooms_list.append(tag.find_next(class_="bed").get_text(strip=True))
        bathrooms_list.append(tag.find_next(class_="bath").get_text(strip=True))
print("Bedrooms:\n", bedrooms_list)
print("Bathrooms:\n", bathrooms_list)

# Get property type, furnishing, and build year
# Get list of all HTML tags that contain type, furnishing, and build year (identified by ul tags with a specific class)
property_type_furnishing_year_tags = soup.find_all("ul", {"class": "listing-property-type"})
# Get list of property type, furnishing, and build year
property_type_furnishing_year_list = [tag.get_text() for tag in property_type_furnishing_year_tags]
print("Property type, furnishing, and build year:\n", property_type_furnishing_year_list)

# Get distance to MRT
# Get list of all HTML tags that contain property listing descriptions (identified by div tags with a specific class)
property_listing_tags = soup.find_all("div", {"class": "listing-description"})
# Get list of MRT distances
mrt_distance_list = []
for tag in property_listing_tags:
    # Get HTML tag that contains distance to MRT (identified by unordered list tag with a specific data-automation-id)
    mrt_distance_tag = tag.find("ul", {"data-automation-id": "listing-features-walk"})
    if mrt_distance_tag is None:
        mrt_distance_list.append(None)
    else:
        mrt_distance_list.append(mrt_distance_tag.get_text(strip=True))
print("MRT distance:\n",mrt_distance_list)

# Property agent description
# Get list of all HTML tags that contain property agent descriptions (identified by div tag with a specific class)
agent_description_tags = soup.find_all("div", {"class": "featured-description"})
# Get list of agent descriptions (also remove the "Listed by XYZ agent" part)
agent_description_list = [tag.get_text().split('"')[1] for tag in agent_description_tags]
print("Property agent description:\n", agent_description_list)

# Validation check
print(len(names_list))
print(len(addresses_list))
print(len(prices_list))
print(len(sizes_list))
print(len(bedrooms_list))
print(len(bathrooms_list))
print(len(property_type_furnishing_year_list))
print(len(mrt_distance_list))
print(len(agent_description_list))
