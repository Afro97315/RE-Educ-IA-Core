# app/utils.py
import os
import json
import logging

logger = logging.getLogger(__name__)

def load_json_data(filename):
    base_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', filename)
    
    if not os.path.exists(base_path):
        logger.error(f"Fichier non trouvé : {base_path}")
        raise FileNotFoundError(f"Le fichier {filename} est manquant dans /data")
    
    try:
        with open(base_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            logger.info(f"✅ Chargé : {filename}")
            return data
    except json.JSONDecodeError as e:
        logger.error(f"Erreur JSON dans {filename} : {e}")
        raise ValueError(f"JSON invalide dans {filename}")
