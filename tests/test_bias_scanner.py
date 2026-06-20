# tests/test_bias_scanner.py
# ---------------------------------------------------------------
# TESTS UNITAIRES DU MODULE DETECTORS + ENDPOINT /biasScanner
# ---------------------------------------------------------------

from app.detectors import detect_bias_keywords

SAMPLE_BIASES = {
    "eurocentrisme": ["découverte", "découvert", "sauvage", "primitif"],
    "invisibilisation": ["sans histoire", "pas de civilisation"]
}

def test_bias_scanner_detects_discovery(client):
    """Teste que 'découvert' est classe comme eurocentrisme et reformule"""
    rv = client.post('/biasScanner', json={
        "text": "Les Européens ont découvert l'Afrique."
    })
    json_data = rv.get_json()
    assert rv.status_code == 200
    assert "eurocentrisme" in json_data["detected_biases"]
    assert "prise de contact" in json_data["suggested_reformulation"]

def test_detector_direct_sauvage():
    """Teste la detection directe du mot sauvage (pluriel)"""
    result = detect_bias_keywords("Ces peuples sauvages vivaient en foret.", SAMPLE_BIASES)
    assert "eurocentrisme" in result

def test_detector_no_bias():
    """Teste qu'un texte neutre ne declenche aucun biais"""
    result = detect_bias_keywords("Les societes africaines avaient des structures complexes.", SAMPLE_BIASES)
    assert result == {}

def test_detector_multiple_biases():
    """Teste la detection de plusieurs categories simultanement"""
    result = detect_bias_keywords(
        "Ces primitifs etaient sans histoire et sauvages.",
        SAMPLE_BIASES
    )
    assert "eurocentrisme" in result
    assert "invisibilisation" in result
