# app/utils.py
# ---------------------------------------------------------------
# FONCTIONS UTILITAIRES PARTAGEES
# load_json_data : charge un fichier JSON depuis le dossier /data
# Ce module est importe par main.py pour lire biases, contexts, reformulations.
# ---------------------------------------------------------------

import os
import json
import logging

logger = logging.getLogger(__name__)

def load_json_data(filename):
    """
    Charge un fichier JSON depuis le dossier /data a la racine du projet.
    Leve FileNotFoundError si absent, ValueError si JSON malformed.
    """
    # os.path.dirname(__file__) = dossier app/
    # on remonte d'un niveau pour atteindre la racine du projet, puis /data
    base_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', filename)

    if not os.path.exists(base_path):
        logger.error(f"Fichier non trouve : {base_path}")
        raise FileNotFoundError(f"Le fichier {filename} est manquant dans /data")

    try:
        with open(base_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            logger.info(f"Charge avec succes : {filename}")
            return data
    except json.JSONDecodeError as e:
        logger.error(f"Erreur JSON dans {filename} : {e}")
        raise ValueError(f"JSON invalide dans {filename}")
