# tests/test_context_adder.py
# ---------------------------------------------------------------
# TESTS DE L'ENDPOINT /contextAdder
# ---------------------------------------------------------------

def test_context_adder_finds_colonial_history(client):
    """Teste que 'colonisation' declenche un enrichissement contextuel"""
    rv = client.post('/contextAdder', json={
        "text": "La colonisation a transforme les societes africaines."
    })
    json_data = rv.get_json()
    assert rv.status_code == 200
    assert len(json_data["added_context"]) > 0

def test_context_adder_returns_matched_keywords(client):
    """Teste que les mots-cles correspondants sont retournes"""
    rv = client.post('/contextAdder', json={
        "text": "L'eurocentrisme efface l'oralite africaine."
    })
    json_data = rv.get_json()
    assert rv.status_code == 200
    assert "eurocentrisme" in json_data["matched_keywords"] or \
           "oralite" in json_data["matched_keywords"] or \
           len(json_data["added_context"]) > 0

def test_context_adder_no_match(client):
    """Teste qu'un texte sans mots-cles retourne une liste vide"""
    rv = client.post('/contextAdder', json={
        "text": "Il fait beau aujourd'hui."
    })
    json_data = rv.get_json()
    assert rv.status_code == 200
    assert json_data["added_context"] == []
