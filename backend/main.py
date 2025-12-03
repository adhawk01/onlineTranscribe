from app import create_app
from app.config import Config

app = create_app()  # Create the Flask app instance

if __name__ == "__main__":
    # Use FLASK_ENV to control mode (defaults to development)
    mode = Config.FLASK_ENV

    if mode == "production":
        cert = Config.SSL_CERT_PATH
        key = Config.SSL_KEY_PATH

        print("[INFO] Running in PRODUCTION mode")
        app.run(host="0.0.0.0", port=Config.PRODUCTION_PORT, ssl_context=(cert, key))

    else:
        print("[INFO] Running in DEVELOPMENT mode (HTTP)")
        app.run(debug=True, port=Config.DEVELOPMENT_PORT)
