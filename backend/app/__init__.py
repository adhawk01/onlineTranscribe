import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from app.config import Config


def create_app():
    app = Flask(
        __name__,
        static_folder="../../frontend/build/static",
        static_url_path="/static"
    )
    app.config.from_object(Config)

    CORS(
        app,
        origins=Config.ALLOWED_ORIGINS,
        supports_credentials=True,
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization"]
    )

    from app.routes.home_routes import home_bp
    app.register_blueprint(home_bp)

    # Only serve React build in production
    if os.getenv("FLASK_ENV") == "production":
        @app.route("/", defaults={"path": ""})
        @app.route("/<path:path>")
        def serve_react(path):
            root_dir = os.path.join(os.path.dirname(__file__), "../../frontend/build")
            if path != "" and os.path.exists(os.path.join(root_dir, path)):
                return send_from_directory(root_dir, path)
            return send_from_directory(root_dir, "index.html")

    return app