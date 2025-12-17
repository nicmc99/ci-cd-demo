import os

# Set APP_VERSION *before* importing the app module,
# because app.py reads APP_VERSION at import time.
os.environ["APP_VERSION"] = "test-version"

from app import app


def test_root_contains_version():
    client = app.test_client()
    resp = client.get("/")
    text = resp.get_data(as_text=True)

    assert resp.status_code == 200
    assert "Hello from Jenkins + Portainer CI/CD!" in text
    assert "test-version" in text


def test_version_endpoint():
    client = app.test_client()
    resp = client.get("/version")

    assert resp.status_code == 200

    data = resp.get_json()
    assert data["version"] == "test-version"
