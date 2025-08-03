# app/__init__.py
# Point d'entrée de l'application Flask

from flask import Flask
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from app.main import app as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
