# tests/conftest.py
import pytest
import sys
from pathlib import Path

# Ajoute le répertoire racine au PYTHONPATH
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

try:
    from app import create_app
except ImportError as e:
    print(f"❌ Erreur d'import : {e}")
    print(f"🐍 Python path : {sys.path}")
    raise

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
