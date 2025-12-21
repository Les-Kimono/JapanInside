"""Tests for the main FastAPI application."""

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_healthcheck():
    """Verify that the root endpoint '/' returns HTTP 200."""
    response = client.get("/")
    assert response.status_code == 200