# tests/conftest.py
# ---------------------------------------------------------------
# CONFIGURATION PYTEST
# Ce fichier est automatiquement lu par pytest avant tous les tests.
# Il definit le "client" de test Flask reutilise dans tous les fichiers de test.
# ---------------------------------------------------------------

import pytest
import sys
from pathlib import Path

# Ajoute le repertoire racine au PYTHONPATH pour que pytest trouve les modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import create_app

@pytest.fixture
def client():
    """Fixture : cree un client de test Flask isole."""
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
