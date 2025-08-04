          # scripts/load_data.py
"""Script de diagnostic : charge les données JSON"""
from app.utils import load_json_data

if __name__ == "__main__":
    print("🔍 Chargement des données...")
    try:
        biases = load_json_data('biases.json')
        contexts = load_json_data('contexts.json')
        reformulations = load_json_data('reformulations.json')
        print("✅ Toutes les données ont été chargées avec succès.")
    except Exception as e:
        print(f"❌ Erreur : {e}")
