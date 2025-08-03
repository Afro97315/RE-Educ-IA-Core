# scripts/load_data.py
"""Script pour charger ou migrer des données"""
from app.utils import load_json_data

if __name__ == "__main__":
    print("Chargement des données...")
    biases = load_json_data('biases.json')
    print(f"{len(biases)} catégories de biais chargées.")
