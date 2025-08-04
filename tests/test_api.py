# tests/test_api.py
def test_home_page(client):
    """Teste la page d'accueil de l'API"""
    response = client.get('/')
    assert response.status_code == 200
    json_data = response.get_json()
    assert "RE-Educ'-IA Core" in json_data["project"]
    assert "biasScanner" in str(json_data["endpoints"])

def test_prompt_injector(client):
    """Teste la génération de prompt inclusif"""
    response = client.get('/promptInjector?topic=Traite+atlantique&perspective=afrocentré')
    assert response.status_code == 200
    json_data = response.get_json()
    assert "afrocentré" in json_data["generated_prompt"]
    assert "Traite atlantique" in json_data["topic"]

def test_role_switch_with_missionaries(client):
    """Teste la reformulation avec le mot 'missionnaires'"""
    response = client.post('/roleSwitch', json={
        "text": "Les missionnaires ont apporté la lumière."
    })
    assert response.status_code == 200
    json_data = response.get_json()
    assert "savoirs ancestraux" in json_data["rephrased_text"]
