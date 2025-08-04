# 📡 Documentation de l'API

Bienvenue dans la documentation de **RE-Educ'-IA-Core**, une API conçue pour détecter et corriger les biais coloniaux, racistes et non inclusifs dans les textes et systèmes d'IA.

Les routes ci-dessous permettent d’analyser, reformuler et repenser les récits historiques et éducatifs depuis des perspectives décoloniales, afrocentrées et inclusives.

---

## `POST /biasScanner` 🔍

Analyse un texte pour détecter les biais lexicaux (eurocentrisme, racisme structurel, invisibilisation) et propose une reformulation inclusive.

### Paramètres
| Champ | Type | Description |
|------|------|-------------|
| `text` | string | Le texte à analyser (obligatoire) |
| `target_perspective` | string | Perspective souhaitée (ex: `afrocentré`, `décolonial`). Par défaut : `afrocentré` |

### Exemple de requête
```json
{
  "text": "Les Européens ont découvert l'Afrique au XVe siècle.",
  "target_perspective": "afrocentré"
}

Réponse Json :
{
  "original_text": "Les Européens ont découvert l'Afrique au XVe siècle.",
  "target_perspective": "afrocentré",
  "detected_biases": ["eurocentrisme"],
  "suggested_reformulation": "Les Européens ont pris contact avec l'Afrique, région déjà peuplée et organisée, au XVe siècle."
}

POST /contextAdder 📚
Ajoute du contexte historique pertinent lorsque certains mots-clés apparaissent dans le texte (ex: "colonisation", "esclavage").

Paramètres
text
string
Le texte à enrichir (obligatoire)

Exemple de requête Json
{
  "text": "Parlons de l'économie esclavagiste des colonies."
}

Réponse Json
{
  "original_text": "Parlons de l'économie esclavagiste des colonies.",
  "added_context": [
    "Le commerce transatlantique des esclaves a structuré l'économie de cette région pendant des siècles, avec des conséquences durables."
  ]
}

POST /roleSwitch 🔄
Reformule un texte en inversant le regard colonial, en adoptant une perspective décoloniale ou afrocentrée.

Paramètres
text
string
Le texte à reformuler (obligatoire)
new_perspective
string
Perspective cible (ex:
autochtone
,
féministe noire
). Par défaut :
afrocentré

exemple de requête json
{
  "text": "Les missionnaires ont apporté la lumière aux peuples sauvages.",
  "new_perspective": "afrocentré"
}

{
  "original_text": "Les missionnaires ont apporté la lumière aux peuples sauvages.",
  "rephrased_text": "Les populations locales disposaient de savoirs ancestraux avant l’arrivée des missionnaires."
}

GET /promptInjector 💬
Génère un prompt pédagogique ou critique, adapté à une perspective décoloniale, pour guider une IA ou un enseignement inclusif.

Paramètres
topic
Sujet à explorer
ex:
Traite atlantique
,
Indépendances africaines
perspective
Perspective à adopter
afrocentré
,
décolonial
,
féministe noire
,
autochtone
,
mondialisé
,
intersectionnel
use_case
Objectif du prompt
formation
,
éducation
,
critique
,
default

Exemple d'URL
/promptInjector?topic=Indépendance%20de%20l'Algérie&perspective=décolonial&use_case=critique

Json
{
  "use_case": "critique",
  "perspective": "décolonial",
  "topic": "Indépendance de l'Algérie",
  "generated_prompt": "Analyse les biais eurocentrés dans le récit dominant de Indépendance de l'Algérie."
}
