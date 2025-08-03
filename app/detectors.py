# app/detectors.py
import re

def detect_bias_keywords(text: str, bias_dict: dict) -> dict:
    """Détecte les biais par mots-clés"""
    results = {}
    text_lower = text.lower()
    for bias, keywords in bias_dict.items():
        matches = [kw for kw in keywords if re.search(r'\b' + re.escape(kw.lower()) + r'\b', text_lower)]
        if matches:
            results[bias] = matches
    return results
