from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
import xgboost  # required to use the XGBoost model loaded from a pickle file
import pickle
import requests
import numpy as np
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get Google Maps API key from .env
google_maps_api_key = os.getenv("google_maps_api_key")

# Create the Flask web application
app = Flask(__name__)

# Set Flask secret key (from .env) for security purposes (e.g. protecting against CSRF attacks)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

# Load XGBoost model from pickle file
with open("models/xgboost.pkl", "rb") as file:
    model = pickle.load(file)


# Create function to get latitude and longitude from an address
def get_latitude_longitude(address):
    # Base URL for the Google Maps Geocoding API
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"

    # Parameters for the Geocoding API request
    params = {
        "address": f"{address}, Singapore",
        "key": google_maps_api_key
    }

    # Send Geocoding API request and store the response
    response = requests.get(base_url, params=params)
    data = response.json()

    # Check if request was successful
    if data["status"] == "OK":
        # Extract latitude and longitude from the response
        location = data["results"][0]["geometry"]["location"]
        latitude = location["lat"]
        longitude = location["lng"]
    else:
        # Assign missing values and print error message if the request failed
        latitude = np.nan
        longitude = np.nan
        print(f"Geocoding request failed for {address}")

    # Return latitude and longitude
    return latitude, longitude


# Create function to get meters to central business district from property latitude and longitude
def get_meters_to_cbd(property_latitude, property_longitude):
    # Return a missing value if latitude or longitude is missing
    if np.isnan(property_latitude) or np.isnan(property_longitude):
        print(f"Property latitude or longitude missing. Assigning missing value for meters to CBD.")
        return np.nan

    # Latitude and longitude of central business district (i.e. Raffles Place)
    cbd_latitude = 1.284184
    cbd_longitude = 103.85151

    # Base URL for the Google Maps Distance Matrix API
    base_url = "https://maps.googleapis.com/maps/api/distancematrix/json"

    # Parameters for the Distance Matrix API request
    params = {
        "origins": f"{property_latitude},{property_longitude}",
        "destinations": f"{cbd_latitude},{cbd_longitude}",
        "key": google_maps_api_key
    }

    # Send the Distance Matrix API request and store the response
    response = requests.get(base_url, params=params)
    data = response.json()

    # Process the response to get the distance
    if "rows" in data and data["rows"]:
        meters_to_cbd = data["rows"][0]["elements"][0]["distance"]["value"]
        print(f"Distance between property and CBD: {meters_to_cbd} meters")
    else:
        print("No distance information available.")
        return np.nan
    return meters_to_cbd


# Create function to get latitude and longitude of the closest school from property latitude and longitude
def get_school_location(property_latitude, property_longitude):
    # Return missing value if latitude or longitude is missing
    if np.isnan(property_latitude) or np.isnan(property_longitude):
        print(f"Property latitude or longitude missing. Assigning missing values for school latitude and longitude.")
        return np.nan, np.nan

    # Base URL for the Google Maps Places Nearby Search API
    base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

    # Parameters for the Nearby Search API request
    params = {
        "location": f"{property_latitude},{property_longitude}",
        "radius": 1000,  # Search radius in meters
        "type": "school",
        "key": google_maps_api_key
    }

    # Send the Nearby Search API request and store the response
    response = requests.get(base_url, params=params)
    data = response.json()

    # Extract latitude and longitude of the closest school from the response
    if "results" in data and data["results"]:
        closest_school = data["results"][0]
        school_name = closest_school["name"]
        school_location = closest_school["geometry"]["location"]
        school_latitude = school_location["lat"]
        school_longitude = school_location["lng"]
        print(f"Closest school: {school_name}")
        print(f"Latitude: {school_latitude}, Longitude: {school_longitude}")
    else:
        school_latitude = np.nan
        school_longitude = np.nan
        print("No schools found nearby.")
    return school_latitude, school_longitude


# Create function to get meters to the closest school
def get_meters_to_school(property_latitude, property_longitude, school_latitude, school_longitude):
    # Return missing value if property latitude or longitude is missing
    if np.isnan(property_latitude) or np.isnan(property_longitude):
        print(f"Property latitude or longitude missing. Assigning missing value for meters to school.")
        return np.nan

    # Return missing value if the school location is missing
    if np.isnan(school_latitude) or np.isnan(school_longitude):
        print(f"School latitude or longitude missing. Assigning missing value for meters to school.")
        return np.nan

    # Base URL for the Google Maps Distance Matrix API
    base_url = "https://maps.googleapis.com/maps/api/distancematrix/json"

    # Parameters for the Distance Matrix API request
    params = {
        "origins": f"{property_latitude},{property_longitude}",
        "destinations": f"{school_latitude},{school_longitude}",
        "key": google_maps_api_key
    }

    # Send the Distance Matrix API request and store the response
    response = requests.get(base_url, params=params)
    data = response.json()

    # Process the response to get the distance
    if "rows" in data and data["rows"]:
        meters_to_school = data["rows"][0]["elements"][0]["distance"]["value"]
        print(f"Distance between property and closest school: {meters_to_school} meters")
    else:
        print("No distance information available. Assigning missing value for meters to school.")
        return np.nan
    return meters_to_school


# Create function to get the average Google Maps rating of nearby restaurants
def get_restaurants_rating(property_latitude, property_longitude):
    # Return missing value if latitude or longitude is missing
    if np.isnan(property_latitude) or np.isnan(property_longitude):
        print(f"Property latitude or longitude missing. Assigning missing value for restaurants rating.")
        return np.nan

    # Base URL for the Google Maps Places Nearby Search API
    base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

    # Parameters for the Nearby Search API request
    params = {
        "location": f"{property_latitude},{property_longitude}",
        "radius": 1000,  # Search radius in meters
        "type": "restaurant",
        "key": google_maps_api_key
    }

    # Send the Nearby Search API request and store the response
    response = requests.get(base_url, params=params)
    data = response.json()

    # Process the response to get the average restaurant rating
    if "results" in data and data["results"]:
        # Extract restaurant ratings as a list, assigning np.nan for missing ratings
        rating_list = [restaurant.get("rating", np.nan) for restaurant in data.get("results")]
        # Calculate average rating, ignoring np.nan values
        average_rating = np.nanmean(rating_list)
        print(f"Number of restaurants: {len(rating_list)}")
        print(f"Number of ratings: {len([rating for rating in rating_list if not np.isnan(rating)])}")
        print(f"Average rating: {average_rating:.2f}")
    else:
        print("No restaurants found nearby. Assigning missing value for restaurants rating.")
        return np.nan
    return average_rating


# Create a class for rental price estimation forms (that inherits from the Flask WTForm class)
class RentalPriceEstimationForm(FlaskForm):
    size = IntegerField("Size (in sqft):", validators=[DataRequired()])
    bedrooms = SelectField("Bedrooms:",
                           choices=[("Room", "Room"), ("Studio", "Studio"), ("1", "1"), ("2", "2"), ("3", "3"),
                                    ("4", "4"), ("5", "5"), ("6", "6"), ("7+", "7+")],
                           validators=[DataRequired()])
    bathrooms = IntegerField("Bathrooms:", validators=[DataRequired()])
    address = TextAreaField("Address:", validators=[DataRequired()])
    property_type = SelectField("Property type:",
                                choices=[("Condominium", "Condominium"), ("Apartment", "Apartment"),
                                         ("HDB Flat", "HDB Flat"), ("Semi-Detached House", "Semi-Detached House"),
                                         ("Good Class Bungalow", "Good Class Bungalow"),
                                         ("Corner Terrace", "Corner Terrace"),
                                         ("Detached House", "Detached House"),
                                         ("Executive Condominium", "Executive Condominium"),
                                         ("Terraced House", "Terraced House"), ("Bungalow House", "Bungalow House"),
                                         ("Cluster House", "Cluster House")],
                                validators=[DataRequired()])
    furnishing = SelectField("Furnishing:",
                             choices=[("", ""),
                                      ("Fully Furnished", "Fully Furnished"),
                                      ("Partially Furnished", "Partially Furnished"),
                                      ("Unfurnished", "Unfurnished")])
    year = IntegerField("Built year:")
    meters_to_mrt = IntegerField("Meters to MRT:", validators=[DataRequired()])
    agent_description = TextAreaField("Agent description:", validators=[DataRequired()])
    submit = SubmitField("Estimate")


# Home route
@app.route("/", methods=["GET", "POST"])
def home():
    # Create a rental price estimation form
    form = RentalPriceEstimationForm()
    # If the user submits valid input
    if form.validate_on_submit():
        # Get the input data from the form
        size = form.size.data
        bedrooms = form.bedrooms.data
        bathrooms = form.bathrooms.data
        address = form.address.data
        property_type = form.property_type.data
        furnishing = form.furnishing.data
        year = form.year.data
        meters_to_mrt = form.meters_to_mrt.data
        agent_description = form.agent_description.data

        # Engineer location-based features via Google Maps API (Cost: 0.079$ per submitted input)
        latitude, longitude = get_latitude_longitude(address)  # Cost: 0.005$
        meters_to_cbd = get_meters_to_cbd(latitude, longitude)  # Cost: 0.005$
        school_latitude, school_longitude = get_school_location(latitude, longitude)  # Cost: 0.032$
        meters_to_school = get_meters_to_school(latitude, longitude, school_latitude, school_longitude)  # Cost: 0.005$
        restaurants_rating = get_restaurants_rating(latitude, longitude)  # Cost: 0.032$

        # Extract features from the agent description
        high_floor = (lambda string: True if "high floor" in string.lower() else False)(agent_description)
        new = any(keyword in agent_description.lower() for keyword in ["brand new", "new unit"])
        renovated = any(keyword in agent_description.lower() for keyword in ["renovated", "renovation"])
        view = any(keyword in agent_description.lower() for keyword in
                   ["sea view", "seaview", "panoramic view", "unblocked view", "unblock view", "stunning view",
                    "park view", "breathtaking view", "river view", "pool view", "spectacular view", "city view",
                    "greenery view", "gorgeous view"])
        penthouse = (lambda string: True if "penthouse" in string.lower() else False)(agent_description)

        # Handle missing values
        # Bathrooms
        if bathrooms is None:
            # Assume 1 bathroom for a room or studio
            if bedrooms == "Room" or bedrooms == "Studio":
                bathrooms = 1
            # Assume 7 bathrooms for 7 or more bedrooms
            elif bedrooms == "7+":
                bathrooms = 7
            # Else assume the same number as bedrooms
            else:
                bathrooms = int(bedrooms)
        # Latitude and longitude
        # Meters to school: Impute the maximum (i.e. 9689 meters, see data_preprocessing.ipynb)
        meters_to_school = 9689 if np.isnan(meters_to_school) else meters_to_school
        # Meters to MRT: Impute the median (i.e. 450 meters, see data_preprocessing.ipynb)
        meters_to_mrt = 450 if np.isnan(meters_to_mrt) else meters_to_mrt
        # Furnishing: Impute the mode (i.e. "Partially Furnished", see data_preprocessing.ipynb)
        furnishing = "Partially Furnished" if furnishing == "" else furnishing
        # Built year: Impute the median (i.e. 2013, see data_preprocessing.ipynb)
        year = 2013 if year is None else year

        # Convert input data to a list
        input_data = [size, bedrooms, bathrooms, latitude, longitude, meters_to_cbd, meters_to_school,
                      restaurants_rating, property_type, furnishing, year, meters_to_mrt, high_floor,
                      new, renovated, view, penthouse]
        # Estimate rental price based on the model
        prediction = model.predict(input_data)[0][0]
        # Render the estimated rental price in the index.html template
        return render_template("index.html",
                               form=form,
                               prediction=prediction)
    return render_template("index.html", form=form)


# Start the Flask web application
if __name__ == "__main__":
    app.run(debug=True)
