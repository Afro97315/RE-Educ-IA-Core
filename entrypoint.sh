#!/bin/sh
set -e

# Vérifie que le module run.py existe
if ! [ -f "run.py" ]; then
  echo "❌ Erreur : le fichier run.py est manquant. Vérifie la structure du projet."
  exit 1
fi

# Définir un port par défaut si $PORT n'est pas défini
PORT=${PORT:-10000}
echo "🚀 Démarrage de RE-Educ'-IA Core sur le port $PORT"

# Lancer Gunicorn
exec gunicorn --bind "0.0.0.0:$PORT" run:app
