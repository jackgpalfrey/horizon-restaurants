"""Entry point module for api."""
from flask import Flask
from .utils.FSRouter import FSRouter


def main():
    """Run main entry point for api."""
    print("Starting API...")
    app: Flask = Flask("Horizon Restaurants")

    router = FSRouter(app)
    router.load_dir("src/api/routes")

    @app.route("/")
    def index():
        return "<p>Horizon Restaurants</p>"

    app.run(host="0.0.0.0", port=5000, debug=True)
