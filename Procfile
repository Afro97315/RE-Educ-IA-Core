# Procfile
# ---------------------------------------------------------------
# FICHIER DE DEMARRAGE POUR RENDER / HEROKU (sans Docker)
#
# Render et Heroku lisent ce fichier pour savoir comment lancer
# l'application. "web" est le type de processus expose sur Internet.
#
# Gunicorn est le serveur WSGI de production pour Flask.
# NE JAMAIS utiliser "python run.py" en production (serveur de dev).
# ---------------------------------------------------------------
web: gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 60 run:app
