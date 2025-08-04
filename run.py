#!/usr/bin/env python3
"""
run.py — Point d'entrée de l'API RE-Educ'-IA Core
Lancé par Gunicorn en production.
"""

import os
from app import create_app

# Crée l'application Flask
app = create_app()

# Point d'entrée pour exécution directe (mode développement)
if __name__ == '__main__':
    # Récupère le port depuis Render ou utilise 10000 en local
    port = int(os.environ.get('PORT', 10000))
    
    # Affiche un message de démarrage clair
    print(f"\n🚀 RE-Educ'-IA Core démarré sur le port {port}")
    print("🌍 API pour décoloniser les récits historiques")
    print("💡 Endpoints : /biasScanner, /contextAdder, /roleSwitch, /promptInjector\n")
    
    # Démarrage du serveur
    app.run(
        host='0.0.0.0',      # Nécessaire pour Docker/Render
        port=port,           # $PORT sur Render, 10000 en local
        debug=False          # Jamais en production
    )
