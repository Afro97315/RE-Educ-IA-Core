# app/utils.py
import os
import json
import logging

# Configurer un logger
logger = logging.getLogger(__name__)

def load_json_data(filename):
    # Construire le chemin vers data/
    base_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', filename)
    
    # Vérifier que le fichier existe
    if not os.path.exists(base_path):
        logger.error(f"Fichier de données introuvable : {base_path}")
        raise FileNotFoundError(f"Le fichier de données est manquant : {filename}")

    try:
        with open(base_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            logger.info(f"✅ Données chargées : {filename}")
            return data
    except json.JSONDecodeError as e:
        logger.error(f"Erreur de syntaxe JSON dans {filename}: {e}")
        raise ValueError(f"Le fichier {filename} contient un JSON invalide.")
    except Exception as e:
        logger.error(f"Erreur inattendue lors du chargement de {filename}: {e}")
        raise
