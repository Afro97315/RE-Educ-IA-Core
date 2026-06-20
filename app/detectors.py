# app/detectors.py
# ---------------------------------------------------------------
# MODULE DE DETECTION DES BIAIS
# Ce module est importe par main.py pour analyser les textes.
# Il est separe de main.py pour respecter la separation des responsabilites.
#
# CORRECTION : la detection par \b (word boundary) ratait les formes
# plurielles (ex: "sauvages" non detecte via le mot-cle "sauvage").
# On utilise desormais re.search sans \b de fin pour capturer prefixes/pluriels.
# ---------------------------------------------------------------

import re
import unicodedata

def normalize(s: str) -> str:
    """Retire les accents pour une comparaison robuste."""
    return unicodedata.normalize('NFD', s).encode('ascii', 'ignore').decode('utf-8').lower()

def detect_bias_keywords(text: str, bias_dict: dict) -> dict:
    """
    Detecte les biais dans un texte par correspondance de mots-cles.

    Parametres :
        text      : le texte a analyser
        bias_dict : dictionnaire {categorie_biais: [liste_de_mots_cles]}

    Retourne :
        dict {categorie_biais: [mots_cles_detectes]}

    Strategie :
        Pour chaque mot-cle, on cherche une correspondance au debut d'un mot
        (prefixe). Cela permet de detecter "sauvages" via "sauvage",
        "decouvert" via "decouvert", etc.
        La normalisation supprime les accents pour rendre la detection robuste.
    """
    results = {}
    text_norm = normalize(text)

    for bias_category, keywords in bias_dict.items():
        matches = []
        for kw in keywords:
            kw_norm = normalize(kw)
            # \b au debut + pas de \b a la fin : capture le mot et ses formes fleechies
            pattern = r'\b' + re.escape(kw_norm)
            if re.search(pattern, text_norm):
                matches.append(kw)
        if matches:
            results[bias_category] = matches

    return results
