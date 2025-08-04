# scripts/load_data.py
"""
Script pour charger ou migrer des données JSON.
Utilisé pour valider que les fichiers dans /data sont accessibles et valides.
"""

from app.utils import load_json_data
import logging

# Configurer un logger simple
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    print("🚀 Chargement des données depuis /data...")

    files = ['biases.json', 'contexts.json', 'reformulations.json']
    for filename in files:
        try:
            data = load_json_data(filename)
            if isinstance(data, dict):
                print(f"✅ {filename} chargé : {len(data)} entrées")
                logger.info(f"Structure OK pour {filename}")
            else:
                print(f"⚠️ {filename} chargé, mais format inattendu (pas un dictionnaire)")
        except FileNotFoundError as e:
            logger.error(f"❌ Fichier manquant : {e}")
            print(f"❌ Échec : {filename} est introuvable. Vérifie le dossier data/")
            return
        except ValueError as e:
            logger.error(f"❌ JSON invalide dans {filename} : {e}")
            print(f"❌ Échec : {filename} contient un JSON mal formaté.")
            return
        except Exception as e:
            logger.error(f"❌ Erreur inattendue : {e}")
            print(f"❌ Échec critique : {e}")
            return

    print("🎉
