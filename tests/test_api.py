# tests/test_api.py
# ---------------------------------------------------------------
# TESTS DE L'API - ROUTES PRINCIPALES
# Lance avec : pytest tests/
# ---------------------------------------------------------------

def test_home_page(client):
    """Teste la page d'accueil de l'API"""
    response = client.get('/')
    assert response.status_code == 200
    json_data = response.get_json()
    assert "RE-Educ-IA Core" in json_data["project"]
    assert "biasScanner" in str(json_data["endpoints"])

def test_prompt_injector(client):
    """Teste la generation de prompt decolonise"""
    response = client.get('/promptInjector?topic=Traite+atlantique&perspective=afrocentre')
    assert response.status_code == 200
    json_data = response.get_json()
    assert "afrocentre" in json_data["generated_prompt"]
    assert "Traite atlantique" in json_data["topic"]

def test_role_switch_with_missionaries(client):
    """Teste la reformulation avec le mot missionnaires"""
    response = client.post('/roleSwitch', json={
        "text": "Les missionnaires ont apporte la lumiere."
    })
    assert response.status_code == 200
    json_data = response.get_json()
    assert "savoirs ancestraux" in json_data["rephrased_text"]

def test_bias_scanner_detects_eurocentrism(client):
    """Teste que 'sauvage' est detecte comme biais eurocentrique"""
    response = client.post('/biasScanner', json={
        "text": "Ces peuples sauvages n'avaient pas de civilisation."
    })
    assert response.status_code == 200
    json_data = response.get_json()
    assert "eurocentrisme" in json_data["detected_biases"]

def test_bias_scanner_invalid_perspective(client):
    """Teste le rejet d'une perspective invalide"""
    response = client.post('/biasScanner', json={
        "text": "Un texte quelconque.",
        "target_perspective": "perspective_inconnue"
    })
    assert response.status_code == 400

def test_context_adder_finds_keyword(client):
    """Teste que colonisation declenche un contexte"""
    response = client.post('/contextAdder', json={
        "text": "La colonisation a transforme les societes africaines."
    })
    assert response.status_code == 200
    json_data = response.get_json()
    assert len(json_data["added_context"]) > 0

def test_missing_text_field(client):
    """Teste la validation des champs requis"""
    response = client.post('/biasScanner', json={"target_perspective": "afrocentre"})
    assert response.status_code == 400

def test_empty_json_body(client):
    """Teste le comportement sans corps JSON"""
    response = client.post('/biasScanner', data="pas du json", content_type="text/plain")
    assert response.status_code == 400
