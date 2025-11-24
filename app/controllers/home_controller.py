# Import necessary Flask functions
from flask import Blueprint, render_template

# Create a Blueprint for home routes
# "home" is the name of the blueprint
# __name__ helps Flask locate resources (like templates) relative to this file
homepage_bp = Blueprint("homepage", __name__)


# Define a route for the root URL "/"
# This function will be called when a user visits the home page
@homepage_bp.route("/")
def home():
    # Render the "homepage.html" template from the templates/ folder
    return render_template("homepage.html")
