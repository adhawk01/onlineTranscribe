# Import the Flask class to create the app
from flask import Flask

# Import the home blueprint (controller) that handles the "/" route
from app.controllers.home_controller import homepage_bp
from app.controllers.subtitles_controller import subtitles_bp


# Factory function to create and configure the Flask app
def create_app():
    # Initialize the Flask application
    app = Flask(__name__)

    # config
    app.config["UPLOAD_DIR"] = "uploads"

    # Register the  blueprints, which contains route(s) like "/" etc..
    app.register_blueprint(homepage_bp)
    app.register_blueprint(subtitles_bp)

    # Return the configured app instance
    return app

