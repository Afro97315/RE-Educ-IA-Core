# config.py
# ---------------------------------------------------------------
# CONFIGURATION CENTRALE DE L'APPLICATION
# Ce fichier centralise tous les parametres de l'app Flask.
# La classe Config est chargee dans app/__init__.py via :
#   app.config.from_object(Config)
#
# En production (Render, Railway, Heroku...), definissez la
# variable d'environnement SECRET_KEY avec une valeur secrete.
# ---------------------------------------------------------------

import os

class Config:
    # Cle secrete Flask : protege les sessions et les tokens CSRF
    # OBLIGATOIRE en production : definir SECRET_KEY dans les variables d'env
    SECRET_KEY = os.environ.get('SECRET_KEY') or 're-educ-ia-secret-key-changez-moi-en-production'

    # Ne pas trier les cles JSON alphabetiquement (preserves l'ordre d'insertion)
    JSON_SORT_KEYS = False

    # Encodage UTF-8 pour les reponses JSON (accents, caracteres africains...)
    JSON_AS_ASCII = False
