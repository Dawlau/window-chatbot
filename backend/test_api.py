from flask import json, Flask
from typing import Generator
from app import app
import pytest


@pytest.fixture
def test_client() -> Generator[Flask.test_client, None, None]:
    """
    Fixture to provide a test client for the Flask app.
    
    Yields:
        Flask.test_client: A test client for the Flask app.
    """
    with app.test_client() as c:
        yield c


def test_api_health(test_client: Flask.test_client) -> None:
    """
    Test the /api/health endpoint for successful health check.
    
    Args:
        test_client (Flask.test_client): The Flask test client.
    """
    response = test_client.get("/api/health")  
    assert response.status_code == 200  
    data = json.loads(response.data)  
    assert data["status"] == "healthy"


def test_chat_endpoint_success(test_client: Flask.test_client) -> None:
    """
    Test the /api/chat endpoint for successful chat interaction.
    
    Args:
        test_client (Flask.test_client): The Flask test client.
    """
    question = "How are you?"
    data = json.dumps({"question": question})
    response = test_client.post("/api/chat", data=data, content_type="application/json")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "response" in data
    assert len(data["response"]) > 0


def test_chat_endpoint_failure(test_client: Flask.test_client) -> None:
    """
    Test the /api/chat endpoint for failure due to missing question.
    
    Args:
        test_client (Flask.test_client): The Flask test client.
    """
    data = json.dumps({})
    response = test_client.post("/api/chat", data=data, content_type="application/json")
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data["error"] == "No question provided"
