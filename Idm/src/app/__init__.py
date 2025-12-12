from flask import Flask
from app.main import register_routes
def create_app():
    app = Flask(__name__)
    register_routes(app)

    return app
