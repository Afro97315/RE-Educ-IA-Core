# app/main.py
from flask import Blueprint, request, jsonify
import os
import re

# Charger les données depuis les fichiers JSON
from app.utils import load_json_data

main_blueprint = Blueprint('main', __name__)

# Charger les données
BIASES_LIST = load_json_data('biases.json')
CONTEXT_DB = load_json_data('contexts.json')
REFORMULATIONS_RAW = load_json_data('reformulations.json')

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
        if field not in data:
            errors.append(f"Le champ '{field}' est requis.")
    return errors

@main_blueprint.route('/')
def home():
    return jsonify({
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
    })

@main_blueprint.route('/biasScanner', methods=['POST'])
def bias_scanner():
    data = request.get_json()
    errors = validate_request(data)
    if errors:
        return jsonify({"error": errors}), 400

    text = data['text']
    target_perspective = data.get('target_perspective', 'afrocentré').lower()

    if target_perspective not in VALID_PERSPECTIVES:
        return jsonify({
            "error": f"Perspective invalide. Choix possibles : {VALID_PERSPECTIVES}"
        }), 400

    detected_biases = []
    text_lower = text.lower()
    for bias, keywords in BIASES_LIST.items():
        for keyword in keywords:
            if re.search(r'\b' + re.escape(keyword.lower()) + r'\b', text_lower):
                detected_biases.append(bias)

    reformulated = text
    for pattern, replacement in REFORMULATIONS_MAP.items():
        reformulated = pattern.sub(replacement, reformulated)

    return jsonify({
        "original_text": text,
        "target_perspective": target_perspective,
        "detected_biases": list(set(detected_biases)),
        "suggested_reformulation": reformulated.strip()
    })

@main_blueprint.route('/contextAdder', methods=['POST'])
def context_adder():
    data = request.get_json()
    errors = validate_request(data)
    if errors:
        return jsonify({"error": errors}), 400

    text = data['text'].lower()
    added_contexts = [ctx for kw, ctx in CONTEXT_DB.items() if kw.lower() in text]

    return jsonify({
        "original_text": data['text'],
        "added_context": list(set(added_contexts))
    })

@main_blueprint.route('/roleSwitch', methods=['POST'])
def role_switch():
    data = request.get_json()
    errors = validate_request(data)
    if errors:
        return jsonify({"error": errors}), 400

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

    return jsonify({
        "original_text": text,
        "rephrased_text": rephrased
    })

@main_blueprint.route('/promptInjector', methods=['GET'])
def prompt_injector():
    topic = request.args.get('topic', 'Histoire').strip()
    perspective = request.args.get('perspective', 'afrocentré').lower()
    use_case = request.args.get('use_case', 'default').lower()

    if perspective not in VALID_PERSPECTIVES:
        return jsonify({
            "error": f"Perspective invalide. Choix possibles : {VALID_PERSPECTIVES}"
        }), 400

    template = PROMPT_TEMPLATES.get(use_case, PROMPT_TEMPLATES['default'])
    return jsonify({
        "use_case": use_case,
        "perspective": perspective,
        "topic": topic,
        "generated_prompt": template.format(topic=topic, perspective=perspective)
    })
