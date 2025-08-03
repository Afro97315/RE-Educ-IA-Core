# tests/test_bias_scanner.py
def test_bias_scanner_detects_discovery(client):
    rv = client.post('/biasScanner', json={
        "text": "Les Européens ont découvert l'Afrique."
    })
    json_data = rv.get_json()
    assert rv.status_code == 200
    assert "eurocentrisme" in json_data["detected_biases"]
    assert "prise de contact" in json_data["suggested_reformulation"]
