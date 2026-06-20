# diagnose.py
# ---------------------------------------------------------------
# SCRIPT DE DIAGNOSTIC AU DEMARRAGE
# Lance ce script avant run.py pour verifier que tout est en ordre.
# Usage : python diagnose.py
# CORRECTION BUG #5 : le script original etait coupe (SyntaxError)
# ---------------------------------------------------------------

import os
import sys
import json

print("DEBUT DU DIAGNOSTIC RE-Educ-IA Core")
print(f"Python version: {sys.version}")
print(f"Repertoire courant: {os.getcwd()}")
print("Contenu du repertoire :")
for item in os.listdir('.'):
    print(f"  {item}/" if os.path.isdir(item) else f"  {item}")

# 1. Verifie que data/ existe
data_dir = 'data'
if not os.path.exists(data_dir):
    print(f"ERREUR : Le dossier '{data_dir}' est introuvable !")
    sys.exit(1)
print(f"OK : Le dossier '{data_dir}' existe.")

# 2. Liste les fichiers dans data/
print(f"Fichiers dans {data_dir}/ : {os.listdir(data_dir)}")

# CORRECTION : le fichier attendu est "context_db.json" et non "contexts.json"
files_required = ['biases.json', 'context_db.json', 'reformulations.json']

for filename in files_required:
    filepath = os.path.join(data_dir, filename)
    if not os.path.exists(filepath):
        print(f"ERREUR : '{filepath}' est manquant !")
        sys.exit(1)
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"OK : '{filename}' charge ({len(data)} entrees)")
    except json.JSONDecodeError as e:
        print(f"ERREUR JSON dans '{filename}' : {e}")
        sys.exit(1)

# 3. Verifie flask et flask-cors
try:
    import flask
    print(f"OK : Flask {flask.__version__} disponible")
except ImportError:
    print("ERREUR : Flask n'est pas installe. Lancez : pip install -r requirements.txt")
    sys.exit(1)

try:
    import flask_cors
    print("OK : flask-cors disponible")
except ImportError:
    print("ERREUR : flask-cors n'est pas installe. Lancez : pip install flask-cors")
    sys.exit(1)

print("\nDIAGNOSTIC TERMINE : tout est en ordre. Vous pouvez lancer run.py")
