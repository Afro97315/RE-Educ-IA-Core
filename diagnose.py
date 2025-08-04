# diagnose.py
"""
Script de diagnostic : vérifie tout ce qui peut planter au démarrage
"""
import os
import sys
import json

print("🔍 DÉBUT DU DIAGNOSTIC")
print(f"🐍 Python version: {sys.version}")
print(f"📦 Répertoire courant: {os.getcwd()}")
print(f"📁 Contenu du répertoire:")
for item in os.listdir('.'):
    print(f"  - {item}/" if os.path.isdir(item) else f"  - {item}")

# 1. Vérifie que data/ existe
data_dir = 'data'
if not os.path.exists(data_dir):
    print(f"❌ ERREUR : Le dossier '{data_dir}' est introuvable !")
    sys.exit(1)
print(f"✅ Le dossier '{data_dir}' existe.")

# 2. Liste les fichiers dans data/
print(f"📄 Fichiers dans {data_dir}/ : {os.listdir(data_dir)}")

# 3. Vérifie chaque JSON
files = ['biases.json', 'contexts.json', 'reformulations.json']
for filename in files:
    filepath
