"""Entry point module for api."""
from flask import Flask
from .utils.FSRouter import FSRouter

SESSION_KEY = "joe"

def main():
    """Run main entry point for api."""
    print("Starting API...")
    app: Flask = Flask("Horizon Restaurants")
    app.secret_key = SESSION_KEY

    # If you want sessions to last longer than a browser sessions
    # app.config["PERMANENT_SESSION_LIFETIME"] = datetime.timedelta(days=3)

    router = FSRouter(app)
    router.load_dir("src/api/routes")

    app.run(host="0.0.0.0", port=5000, debug=True)
