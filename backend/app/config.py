import os
from dotenv import load_dotenv

# Load .env values
load_dotenv()

class Config:
    # 🌍 General
    FLASK_ENV = os.getenv("FLASK_ENV", "production")
    APP_NAME = os.getenv("APP_NAME", "OnlineTranscribe")
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback-insecure-key")

    # 🧰 Ports
    DEVELOPMENT_PORT = int(os.getenv("DEV_PORT", 5050))
    PRODUCTION_PORT = int(os.getenv("PROD_PORT", 5001))
    REACT_DEV_PORT = int(os.getenv("REACT_DEV_PORT", 3000))


    # 🔒 SSL
    SSL_CERT_PATH = os.getenv("SSL_CERT_PATH")
    SSL_KEY_PATH = os.getenv("SSL_KEY_PATH")

    # 🧩 CORS
    ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

    # 🗄️ Database
    DB_HOST = os.getenv("DB_HOST")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")