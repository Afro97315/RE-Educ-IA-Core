# tests/conftest.py
import pytest
import sys
from pathlib import Path

# Ajoute le répertoire racine au PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
