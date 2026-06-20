#!/usr/bin/env python3
# run.py
# ---------------------------------------------------------------
# POINT D'ENTREE DE L'API RE-EDUC-IA CORE
# ---------------------------------------------------------------
# En DEVELOPPEMENT : python run.py
# En PRODUCTION    : gunicorn run:app --bind 0.0.0.0:$PORT
#
# Ce fichier cree l'instance Flask via la fabrique create_app()
# definie dans app/__init__.py, puis la demarre.
# ---------------------------------------------------------------

import os
from app import create_app

# Creation de l'application Flask (enregistrement des routes, CORS, config)
app = create_app()

if __name__ == '__main__':
    # En local, le port par defaut est 10000 (compatible Render)
    # Sur Render/Railway, la variable $PORT est injectee automatiquement
    port = int(os.environ.get('PORT', 10000))

    print(f"\n[RE-Educ-IA Core] Demarrage sur le port {port}")
    print("[RE-Educ-IA Core] Endpoints disponibles :")
    print("  GET  /")
    print("  POST /biasScanner")
    print("  POST /contextAdder")
    print("  POST /roleSwitch")
    print("  GET  /promptInjector\n")

    # debug=False OBLIGATOIRE en production
    app.run(host='0.0.0.0', port=port, debug=False)
