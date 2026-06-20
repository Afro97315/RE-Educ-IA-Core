# Dockerfile
# ---------------------------------------------------------------
# IMAGE DE PRODUCTION POUR RE-EDUC-IA CORE
#
# Ce fichier decrit comment construire et lancer l'API dans un
# conteneur Docker isole. Utilise par Docker, Render, Railway...
#
# Commandes utiles :
#   docker build -t re-educ-ia .
#   docker run -p 10000:10000 re-educ-ia
# ---------------------------------------------------------------

# Image de base legere Python 3.10 (slim = sans outils inutiles)
FROM python:3.10-slim

# Repertoire de travail dans le conteneur
WORKDIR /app

# Copier les dependances en premier (optimise le cache Docker :
# si requirements.txt n'a pas change, pip ne se relance pas)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le reste du projet
COPY . .

# Port expose par le conteneur (doit correspondre a $PORT ou 10000)
EXPOSE 10000

# CORRECTION BUG : l'ancienne version lancait diagnose.py (script de debug)
# au lieu de l'API. On utilise entrypoint.sh qui lance Gunicorn correctement.
ENTRYPOINT ["sh", "entrypoint.sh"]
