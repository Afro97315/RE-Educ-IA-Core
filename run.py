# run.py
from flask import Flask
import os
import json
import re

# Créer l'app directement ici (pour éviter les problèmes d'import)
app = Flask(__name__)

# Charger les données JSON
def load_json_data(filename):
    base_path = os.path.join(os.path.dirname(__file__), 'data', filename)
    with open(base_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Charger les données
try:
    BIASES_LIST = load_json_data('biases.json')
    CONTEXT_DB = load_json_data('contexts.json')
    REFORMULATIONS_RAW = load_json_data('reformulations.json')
except Exception as e:
    print(f"❌ Erreur de chargement des données : {e}")
    BIASES_LIST = {}
    CONTEXT_DB = {}
    REFORMULATIONS_RAW = {}

# Précompiler les regex
REFORMULATIONS_MAP = {
    re.compile(pattern, re.IGNORECASE): replacement
    for pattern, replacement in REFORMULATIONS_RAW.items()
}

VALID_PERSPECTIVES = [
    'afrocentré',
    'décolonial',
    'féministe noire',
    'autochtone',
    'mondialisé',
    'intersectionnel'
]

PROMPT_TEMPLATES = {
    "formation": "Explique {topic} depuis une perspective {perspective}, en mettant en avant les savoirs endogènes.",
    "éducation": "Raconte {topic} comme on l'enseignerait dans une école valorisant les récits africains.",
    "critique": "Analyse les biais eurocentrés dans le récit dominant de {topic}.",
    "default": "Explore {topic} avec une perspective {perspective}."
}

def validate_request(data, required_fields=['text']):
    errors = []
    for field in required_fields:
        if field not in 
            errors.append(f"Le champ '{field}' est requis.")
    return errors

@app.route('/')
def home():
    return {
        "project": "RE-Educ'-IA Core",
        "description": "API pour détecter et corriger les biais coloniaux, racistes et non inclusifs",
        "version": "1.0.0",
        "endpoints": [
            "/biasScanner (POST)",
            "/contextAdder (POST)",
            "/roleSwitch (POST)",
            "/promptInjector (GET)"
        ],
        "source": "https://github.com/Afro97315/RE-Educ-IA-Core",
        "license": "AGPL-3.0"
    }

@app.route('/biasScanner', methods=['POST'])
def bias_scanner():
    data = request.get_json()
    errors = validate_request(data)
    if errors:
        return {"error": errors}, 400

    text = data['text']
    target_perspective = data.get('target_perspective', 'afrocentré').lower()

    if target_perspective not in VALID_PERSPECTIVES:
        return {
            "error": f"Perspective invalide. Choix possibles : {VALID_PERSPECTIVES}"
        }, 400

    detected_biases = []
    text_lower = text.lower()
    for bias, keywords in BIASES_LIST.items():
        for keyword in keywords:
            if re.search(r'\b' + re.escape(keyword.lower()) + r'\b', text_lower):
                detected_biases.append(bias)

    reformulated = text
    for pattern, replacement in REFORMULATIONS_MAP.items():
        reformulated = pattern.sub(replacement, reformulated)

    return {
        "original_text": text,
        "target_perspective": target_perspective,
        "detected_biases": list(set(detected_biases)),
        "suggested_reformulation": reformulated.strip()
    }

@app.route('/contextAdder', methods=['POST'])
def context_adder():
    data = request.get_json()
    errors = validate_request(data)
    if errors:
        return {"error": errors}, 400

    text = data['text'].lower()
    added_contexts = [ctx for kw, ctx in CONTEXT_DB.items() if kw.lower() in text]

    return {
        "original_text": data['text'],
        "added_context": list(set(added_contexts))
    }

@app.route('/roleSwitch', methods=['POST'])
def role_switch():
    data = request.get_json()
    errors = validate_request(data)
    if errors:
        return {"error": errors}, 400

    text = data['text']
    new_perspective = data.get('new_perspective', 'afrocentré').lower()

    if new_perspective not in VALID_PERSPECTIVES:
        new_perspective = 'afrocentré'

    lower_text = text.lower()
    if "missionnaires" in lower_text:
        rephrased = "Les populations locales disposaient de savoirs ancestraux avant l’arrivée des missionnaires."
    elif "découverte" in lower_text:
        rephrased = "Les terres étaient déjà habitées et organisées avant le contact européen."
    else:
        rephrased = f"[{new_perspective.capitalize()} perspective] " + text

    return {
        "original_text": text,
        "rephrased_text": rephrased
    }

@app.route('/promptInjector', methods=['GET'])
def prompt_injector():
    topic = request.args.get('topic', 'Histoire').strip()
    perspective = request.args.get('perspective', 'afrocentré').lower()
    use_case = request.args.get('use_case', 'default').lower()

    if perspective not in VALID_PERSPECTIVES:
        return {
            "error": f"Perspective invalide. Choix possibles : {VALID_PERSPECTIVES}"
        }, 400

    template = PROMPT_TEMPLATES.get(use_case, PROMPT_TEMPLATES['default'])
    return {
        "use_case": use_case,
        "perspective": perspective,
        "topic": topic,
        "generated_prompt": template.format(topic=topic, perspective=perspective)
    }

# === Démarrage ===
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
