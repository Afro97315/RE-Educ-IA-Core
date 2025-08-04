# 🌍 RE-Educ'-IA Core
![CI](https://github.com/Afro97315/RE-Educ-IA-Core/actions/workflows/ci.yml/badge.svg)
> Une API open source pour détecter et corriger les biais coloniaux, racistes et non inclusifs dans les textes générés par IA.

## 🎯 Objectif
Démanteler les récits eurocentrés, invisibilisateurs et stigmatisants dans les systèmes d'IA, l'éducation et les projets technologiques.

## 🚀 API

- `POST /biasScanner` : Détecte les biais & suggère reformulation
- `POST /contextAdder` : Ajoute du contexte historique
- `POST /roleSwitch` : Reformule avec une perspective décoloniale
- `GET /promptInjector` : Génère des prompts inclusifs

## 📦 Installation

```bash
git clone https://github.com/ton-pseudo/re-educ-ia-core
pip install -r requirements.txt
python app/main.py
