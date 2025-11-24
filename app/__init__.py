# Import the Flask class to create the app
from flask import Flask

# Import the home blueprint (controller) that handles the "/" route
from app.controllers.home_controller import homepage_bp


# Factory function to create and configure the Flask app
def create_app():
    # Initialize the Flask application
    app = Flask(__name__)

    # Register the home blueprint, which contains route(s) like "/"
    app.register_blueprint(homepage_bp)

    # Return the configured app instance
    return app
