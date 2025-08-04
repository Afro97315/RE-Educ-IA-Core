# 📡 Documentation de l'API

## `POST /biasScanner`
Analyse un texte pour détecter les biais.

**Exemple de requête (Body)** :

```json
{
  "text": "La découverte de l'Afrique",
  "target_perspective": "afrocentré"
}
{
  "detected_biases": ["eurocentrisme"],
  "suggested_reformulation": "prise de contact avec une région déjà peuplée et organisée"
}
