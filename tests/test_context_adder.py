# tests/test_context_adder.py
def test_context_adder_finds_colonial_history(client):
    # Données d'entrée
    response = client.post('/contextAdder', json={
        "text": "Parlons de l'histoire coloniale de l'Algérie."
    })

    # Vérifie le statut
    assert response.status_code == 200

    # Récupère les données
    data = response.get_json()

    # Vérifie que added_context existe et n'est pas vide
    assert "added_context" in data
    assert len(data["added_context"]) > 0

    # Vérifie que le contexte contient bien une mention de la colonisation
    context_text = data["added_context"][0].lower()
    assert "colonisation" in context_text or "colonial" in context_text
