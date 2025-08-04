# app/__init__.py
from flask import Flask
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enregistre le blueprint
    from app.main import main_blueprint
    app.register_blueprint(main_blueprint)

    return app
