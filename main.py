import os
from app import create_app
from dotenv import load_dotenv



# 💡 AUTO-INCLUDE DEV SSL SETUP
def run_dev_ssl_setup():
    from scripts import dev_ssl_setup
    dev_ssl_setup.create_dev_ssl_cert()


load_dotenv() # Load environment variables from .env file
app = create_app() # Create the Flask app instance

if __name__ == "__main__":
    # Use FLASK_ENV to control mode (defaults to development)
    mode = os.environ.get("FLASK_ENV")

    if mode == "production":
        cert = os.environ.get("SSL_CERT_PATH")
        key = os.environ.get("SSL_KEY_PATH")

        print("[INFO] Running in PRODUCTION mode")
        app.run(host="0.0.0.0", port=os.environ.get("PORT"), ssl_context=(cert, key))

    else:
        print("[INFO] Running in DEVELOPMENT mode")
        run_dev_ssl_setup()
        app.run(ssl_context=("ssl/cert.pem", "ssl/key.pem"), debug=True)
