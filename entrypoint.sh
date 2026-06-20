#!/bin/sh
# entrypoint.sh
# ---------------------------------------------------------------
# SCRIPT DE DEMARRAGE EN PRODUCTION
# Lance par Docker (ENTRYPOINT) ou directement sur Render/Railway.
#
# Il execute d'abord le diagnostic pour detecter tout probleme
# au demarrage, puis lance Gunicorn (serveur WSGI de production).
# Gunicorn est plus robuste et performant que le serveur Flask dev.
# ---------------------------------------------------------------

set -e

# Verification que run.py est bien present
if ! [ -f "run.py" ]; then
  echo "ERREUR : run.py est manquant."
  exit 1
fi

# Port par defaut si $PORT n'est pas injecte par la plateforme
PORT=${PORT:-10000}

echo "Demarrage de RE-Educ-IA Core sur le port $PORT"

# Lancement de Gunicorn :
#   --bind 0.0.0.0:$PORT  = ecoute sur toutes les interfaces
#   --workers 2           = 2 processus paralleles (adapter selon RAM)
#   --timeout 60          = coupe les requetes qui depassent 60s
#   run:app               = objet Flask "app" dans le fichier run.py
exec gunicorn \
  --bind "0.0.0.0:$PORT" \
  --workers 2 \
  --timeout 60 \
  --access-logfile - \
  --error-logfile - \
  run:app
