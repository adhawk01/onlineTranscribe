# Import necessary Flask functions
from flask import Blueprint, render_template
from app.services.mysql_service import MySQLClass

# Create a Blueprint for home routes
# "homepage" is the name of the blueprint
# __name__ helps Flask locate resources (like templates) relative to this file
homepage_bp = Blueprint("homepage", __name__)


# Define a route for the root URL "/"
# This function will be called when a user visits the home page
@homepage_bp.route("/")
def home():
    db = MySQLClass.getInstance()
    # Render the "homepage.html" template from the templates/ folder
    results = db.select_query("select * from User")
    print(results)
    return render_template("homepage.html")
