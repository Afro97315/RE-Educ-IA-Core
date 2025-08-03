# tests/test_context_adder.py
def test_context_adder_finds_colonial_history(client):
    rv = client.post('/contextAdder', json={
        "text": "Parlons de l'histoire coloniale de l'Algérie."
    })
    json_data = rv.get_json()
    assert "colonisation" in json_data["added_context"][0]
