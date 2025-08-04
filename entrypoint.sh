# entrypoint.sh
#!/bin/sh

# Définir un port par défaut si $PORT n'est pas défini
PORT=${PORT:-10000}

# Lancer Gunicorn avec le port interpolé
exec gunicorn --bind "0.0.0.0:$PORT" run:app
