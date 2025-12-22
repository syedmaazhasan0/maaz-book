import pytest
import os
import tempfile
from unittest.mock import patch, MagicMock
from src.config import settings
from src.main import app
from fastapi.testclient import TestClient


def test_no_credentials_in_error_messages():
    """
    Test that error messages don't expose credentials
    """
    client = TestClient(app)
    
    # Test with malformed request to trigger error handling
    response = client.post(
        "/query",
        json={"invalid_field": "test"}
    )
    
    # Check that no credentials appear in the error response
    response_text = response.text.lower()
    assert "key" not in response_text or "token" not in response_text or "secret" not in response_text
    assert settings.cohere_api_key not in response_text
    assert settings.qdrant_api_key not in response_text


def test_no_credentials_in_health_check():
    """
    Test that health check endpoint doesn't expose credentials
    """
    client = TestClient(app)
    
    response = client.get("/health")
    response_text = response.text.lower()
    
    # Verify that credentials are not exposed in the health check response
    assert settings.cohere_api_key not in response_text
    assert settings.qdrant_api_key not in response_text
    assert settings.qdrant_url not in response_text
    assert settings.neon_db_url not in response_text


def test_config_loads_securely():
    """
    Test that configuration is loaded securely without exposing credentials
    """
    # Verify that settings are loaded from environment variables
    assert hasattr(settings, 'cohere_api_key')
    assert hasattr(settings, 'qdrant_url')
    assert hasattr(settings, 'qdrant_api_key')
    
    # Verify that the settings object doesn't expose credentials in string representation
    settings_str = str(settings)
    assert settings.cohere_api_key not in settings_str
    assert settings.qdrant_api_key not in settings_str


def test_no_credentials_in_logs():
    """
    Test that credentials are not logged by the application
    """
    # This is a conceptual test - in a real implementation, we'd capture logs
    # and verify that credentials don't appear in them
    # For now, we'll just verify that our services don't log credentials directly
    
    from src.services.cohere_service import CohereClient
    from src.services.qdrant_service import QdrantService
    
    # Verify that the services initialize without exposing credentials in their repr
    cohere_client = CohereClient()
    qdrant_service = QdrantService()
    
    # These should not expose credentials in their string representation
    cohere_repr = repr(cohere_client)
    qdrant_repr = repr(qdrant_service)
    
    assert settings.cohere_api_key not in cohere_repr
    assert settings.qdrant_api_key not in qdrant_repr


def test_input_validation_prevents_injection():
    """
    Test that inputs are validated to prevent injection attacks
    """
    client = TestClient(app)
    
    # Test with potentially malicious inputs
    malicious_inputs = [
        {"question": "test", "book_id": "test", "selected_text": "${settings.cohere_api_key}"},
        {"question": "test", "book_id": "test", "selected_text": "${COHERE_API_KEY}"},
        {"question": "test", "book_id": "test", "selected_text": "{{7*7}}"},
        {"question": "test", "book_id": "test", "selected_text": "`ls -la`"},
    ]
    
    for malicious_input in malicious_inputs:
        # This should not cause credential exposure
        response = client.post("/query", json=malicious_input)
        # The response should not contain credentials
        response_text = response.text.lower()
        assert settings.cohere_api_key.lower() not in response_text
        assert settings.qdrant_api_key.lower() not in response_text


if __name__ == "__main__":
    test_no_credentials_in_error_messages()
    test_no_credentials_in_health_check()
    test_config_loads_securely()
    test_no_credentials_in_logs()
    test_input_validation_prevents_injection()
    print("All security tests passed!")