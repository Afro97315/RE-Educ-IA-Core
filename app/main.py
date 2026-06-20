# app/main.py
# ---------------------------------------------------------------
# ROUTES PRINCIPALES DE L'API RE-EDUC-IA CORE
# Ce fichier definit les 4 endpoints de l'API :
#   /biasScanner   : detecte les biais dans un texte
#   /contextAdder  : ajoute du contexte historique / culturel
#   /roleSwitch    : reformule un texte depuis une autre perspective
#   /promptInjector: genere des prompts IA decolonises
# ---------------------------------------------------------------

from flask import Blueprint, request, jsonify
import os
import re
import logging

from app.utils import load_json_data
from app.detectors import detect_bias_keywords  # utilisation du module detectors existant

logger = logging.getLogger(__name__)

main_blueprint = Blueprint('main', __name__)

# ---------------------------------------------------------------
# CHARGEMENT DES DONNEES AU DEMARRAGE
# CORRECTION BUG #1 : le fichier s'appelle "context_db.json"
# et non "contexts.json" (crash au demarrage dans la version originale)
# ---------------------------------------------------------------
BIASES_LIST        = load_json_data('biases.json')
CONTEXT_DB         = load_json_data('context_db.json')   # <-- NOM CORRIGE
REFORMULATIONS_RAW = load_json_data('reformulations.json')

# ---------------------------------------------------------------
# PRECOMPILATION DES REGEX DE REFORMULATION
# CORRECTION BUG #2 : les patterns etaient precompiles sans try/except.
# Un pattern invalide faisait planter toute l'API au demarrage.
# On ignore desormais les patterns defectueux avec un log d'avertissement.
# ---------------------------------------------------------------
REFORMULATIONS_MAP = {}
for pattern_str, replacement in REFORMULATIONS_RAW.items():
    try:
        compiled = re.compile(pattern_str, re.IGNORECASE)
        REFORMULATIONS_MAP[compiled] = replacement
    except re.error as e:
        logger.warning(f"Pattern regex invalide ignore : {pattern_str!r} -> {e}")

# ---------------------------------------------------------------
# CONSTANTES METIER
# ---------------------------------------------------------------
VALID_PERSPECTIVES = [
    'afrocentre',
    'decolonial',
    'feministe noire',
    'autochtone',
    'mondialise',
    'intersectionnel'
]

# Normalisation des accents pour la comparaison des perspectives
# (l'utilisateur peut ecrire "afrocentré" ou "afrocentre")
def normalize(s):
    """Supprime les accents pour une comparaison flexible."""
    import unicodedata
    return unicodedata.normalize('NFD', s).encode('ascii', 'ignore').decode('utf-8').lower()

VALID_PERSPECTIVES_NORMALIZED = [normalize(p) for p in VALID_PERSPECTIVES]
VALID_PERSPECTIVES_DISPLAY = [
    'afrocentre', 'decolonial', 'feministe noire',
    'autochtone', 'mondialise', 'intersectionnel'
]

PROMPT_TEMPLATES = {
    "formation": "Explique {topic} depuis une perspective {perspective}, en mettant en avant les savoirs endogenes.",
    "education": "Raconte {topic} comme on l'enseignerait dans une ecole valorisant les recits africains.",
    "critique":  "Analyse les biais eurocentres dans le recit dominant de {topic}.",
    "default":   "Explore {topic} avec une perspective {perspective}."
}

# ---------------------------------------------------------------
# FONCTION DE VALIDATION
# Verifie que les champs requis sont presents dans la requete JSON.
# ---------------------------------------------------------------
def validate_request(data, required_fields=None):
    if required_fields is None:
        required_fields = ['text']
    if data is None:
        return ["Le corps de la requete doit etre un JSON valide avec Content-Type: application/json"]
    errors = []
    for field in required_fields:
        if field not in data or not str(data[field]).strip():
            errors.append(f"Le champ '{field}' est requis et ne peut pas etre vide.")
    return errors


# ---------------------------------------------------------------
# ROUTE D'ACCUEIL
# ---------------------------------------------------------------
@main_blueprint.route('/')
def home():
    return jsonify({
        "project": "RE-Educ-IA Core",
        "description": "API pour detecter et corriger les biais coloniaux, racistes et non inclusifs",
        "version": "1.1.0",
        "endpoints": [
            "/biasScanner (POST)",
            "/contextAdder (POST)",
            "/roleSwitch (POST)",
            "/promptInjector (GET)"
        ],
        "source": "https://github.com/Afro97315/RE-Educ-IA-Core",
        "license": "AGPL-3.0"
    })


# ---------------------------------------------------------------
# ENDPOINT /biasScanner
# Detecte les biais dans un texte et propose une reformulation.
# Corps JSON : { "text": "...", "target_perspective": "afrocentre" }
# ---------------------------------------------------------------
@main_blueprint.route('/biasScanner', methods=['POST'])
def bias_scanner():
    data = request.get_json(silent=True)  # silent=True evite une exception si JSON malformed
    errors = validate_request(data)
    if errors:
        return jsonify({"error": errors}), 400

    text = data['text'].strip()
    raw_perspective = data.get('target_perspective', 'afrocentre')
    target_perspective_norm = normalize(raw_perspective)

    # CORRECTION BUG #3 : la comparaison des perspectives ignorait les accents
    if target_perspective_norm not in VALID_PERSPECTIVES_NORMALIZED:
        return jsonify({
            "error": f"Perspective invalide : '{raw_perspective}'. "
                     f"Valeurs acceptees : {VALID_PERSPECTIVES_DISPLAY}"
        }), 400

    # Detection des biais via le module detectors.py (reutilise correctement)
    bias_results = detect_bias_keywords(text, BIASES_LIST)
    detected_biases = list(bias_results.keys())

    # Application des reformulations
    reformulated = text
    for pattern, replacement in REFORMULATIONS_MAP.items():
        reformulated = pattern.sub(replacement, reformulated)

    return jsonify({
        "original_text": text,
        "target_perspective": raw_perspective,
        "detected_biases": detected_biases,
        "bias_details": bias_results,          # detail des mots declencheurs par categorie
        "suggested_reformulation": reformulated.strip()
    })


# ---------------------------------------------------------------
# ENDPOINT /contextAdder
# Enrichit un texte avec du contexte historique ou culturel.
# Corps JSON : { "text": "..." }
# ---------------------------------------------------------------
@main_blueprint.route('/contextAdder', methods=['POST'])
def context_adder():
    data = request.get_json(silent=True)
    errors = validate_request(data)
    if errors:
        return jsonify({"error": errors}), 400

    text = data['text'].strip()
    text_lower = text.lower()

    # Recherche de correspondances dans context_db.json
    added_contexts = {}
    for keyword, ctx in CONTEXT_DB.items():
        if keyword.lower() in text_lower:
            added_contexts[keyword] = ctx

    return jsonify({
        "original_text": text,
        "matched_keywords": list(added_contexts.keys()),
        "added_context": list(added_contexts.values())
    })


# ---------------------------------------------------------------
# ENDPOINT /roleSwitch
# Reformule un texte depuis une nouvelle perspective.
# Corps JSON : { "text": "...", "new_perspective": "decolonial" }
# CORRECTION BUG #4 : logique etendue, plus seulement 2 cas hardcodes.
# ---------------------------------------------------------------
@main_blueprint.route('/roleSwitch', methods=['POST'])
def role_switch():
    data = request.get_json(silent=True)
    errors = validate_request(data)
    if errors:
        return jsonify({"error": errors}), 400

    text = data['text'].strip()
    raw_perspective = data.get('new_perspective', 'afrocentre')
    new_perspective_norm = normalize(raw_perspective)

    # Si perspective inconnue, on bascule sur 'afrocentre' par defaut (comportement original preserve)
    if new_perspective_norm not in VALID_PERSPECTIVES_NORMALIZED:
        new_perspective_norm = 'afrocentre'
        raw_perspective = 'afrocentre'

    lower_text = text.lower()

    # Reformulations thematiques etendues
    reformulation_rules = [
        (["missionnaires", "missionnaire"],
         "Les populations locales disposaient de savoirs ancestraux avant l'arrivee des missionnaires europeens."),
        (["decouverte", "découverte", "decouvrir", "découvrir"],
         "Les terres etaient deja habitees, organisees et riches de cultures complexes avant le contact europeen."),
        (["sauvage", "primitif", "arriéré", "arriere", "non civilise", "non civilise"],
         "Ces peuples possedaient des structures sociales, politiques et spirituelles elaborees."),
        (["sous-developpe", "sous développé", "pays pauvre"],
         "Ces pays du Sud ont ete structurallement appauvris par des siecles d'exploitation coloniale."),
        (["tribu", "tribus"],
         "Ces communautes autochtones etaient structurees en nations avec leurs propres gouvernances."),
        (["esclave", "esclaves"],
         "Ces personnes etaient des victimes de la traite, des etre humains depossedes de leur liberte par un systeme economique criminel."),
    ]

    rephrased = None
    for triggers, response_text in reformulation_rules:
        if any(t in lower_text for t in triggers):
            rephrased = response_text
            break

    # Fallback : prefixe de perspective si aucune regle ne correspond
    if rephrased is None:
        # Application des reformulations du fichier JSON si disponibles
        reformulated = text
        for pattern, replacement in REFORMULATIONS_MAP.items():
            reformulated = pattern.sub(replacement, reformulated)
        if reformulated != text:
            rephrased = reformulated
        else:
            rephrased = f"[Perspective {raw_perspective}] {text}"

    return jsonify({
        "original_text": text,
        "new_perspective": raw_perspective,
        "rephrased_text": rephrased
    })


# ---------------------------------------------------------------
# ENDPOINT /promptInjector
# Genere un prompt IA decolonise pret a l'emploi.
# Parametres GET : ?topic=...&perspective=...&use_case=...
# ---------------------------------------------------------------
@main_blueprint.route('/promptInjector', methods=['GET'])
def prompt_injector():
    topic       = request.args.get('topic', 'Histoire').strip()
    raw_persp   = request.args.get('perspective', 'afrocentre').strip()
    use_case    = request.args.get('use_case', 'default').lower().strip()

    perspective_norm = normalize(raw_persp)

    if perspective_norm not in VALID_PERSPECTIVES_NORMALIZED:
        return jsonify({
            "error": f"Perspective invalide : '{raw_persp}'. "
                     f"Valeurs acceptees : {VALID_PERSPECTIVES_DISPLAY}"
        }), 400

    template = PROMPT_TEMPLATES.get(use_case, PROMPT_TEMPLATES['default'])

    return jsonify({
        "use_case": use_case,
        "perspective": raw_persp,
        "topic": topic,
        "generated_prompt": template.format(topic=topic, perspective=raw_persp)
    })
