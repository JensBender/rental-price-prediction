from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
import xgboost  # required to use the XGBoost model loaded from a pickle file
import pickle
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Create the Flask web application
app = Flask(__name__)

# Set Flask secret key (stored in .env) for security purposes (e.g. protecting against CSRF attacks)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

# Load XGBoost model from pickle file
with open("models/xgboost.pkl", "rb") as file:
    model = pickle.load(file)


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
                                         ("Good Class Bungalow", "Good Class Bungalow"), ("Corner Terrace", "Corner Terrace"),
                                         ("Detached House", "Detached House"), ("Executive Condominium", "Executive Condominium"),
                                         ("Terraced House", "Terraced House"), ("Bungalow House", "Bungalow House"),
                                         ("Cluster House", "Cluster House")],
                                validators=[DataRequired()])
    furnishing = SelectField("Furnishing:",
                             choices=[("Fully Furnished", "Fully Furnished"),
                                      ("Partially Furnished", "Partially Furnished"),
                                      ("Unfurnished", "Unfurnished")],
                             validators=[DataRequired()])
    year = IntegerField("Built year:", validators=[DataRequired()])
    meters_to_mrt = IntegerField("Meters to MRT:", validators=[DataRequired()])
    agent_description = TextAreaField("Agent description:", validators=[DataRequired()])
    submit = SubmitField("Estimate")


# Home route
@app.route("/", methods=["GET", "POST"])
def home():
    # Create a rental price estimation form
    form = RentalPriceEstimationForm()
    # If the user submits valid information in the form
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

        # Engineer location-based features
        latitude = None  # get from address using Google Maps API
        longitude = None  # get from address using Google Maps API
        meters_to_cbd = None  # get from latitude and longitude using Google Maps API
        meters_to_school = None  # get from latitude and longitude using Google Maps API
        restaurants_rating = None   # get from latitude and longitude using Google Maps API

        # Extract features from agent description
        high_floor = None
        new = None
        renovated = None
        view = None
        penthouse = None

        # Handle missing values

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
