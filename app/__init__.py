# app/__init__.py
# ---------------------------------------------------------------
# POINT D'ENTREE DE L'APPLICATION FLASK
# Ce fichier cree l'instance Flask et enregistre les routes (Blueprint).
# Il est appele par run.py au demarrage.
# ---------------------------------------------------------------

from flask import Flask
from flask_cors import CORS  # CORRECTION : ajout CORS pour autoriser les appels depuis un front-end
from config import Config

def create_app():
    """Fabrique d'application Flask (pattern Application Factory)."""
    app = Flask(__name__)
    app.config.from_object(Config)

    # CORS : autorise tous les domaines a interroger l'API
    # En production, remplacez "*" par votre domaine (ex: "https://monsite.netlify.app")
    CORS(app, origins="*")

    # Enregistrement du blueprint principal (toutes les routes)
    from app.main import main_blueprint
    app.register_blueprint(main_blueprint)

    return app
