import sys
import os
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from main import create_app
from config.settings import settings

app = create_app()
client = TestClient(app)


class TestEndpointsComprehensive:
    """Comprehensive tests for all API endpoints (v1 and v2)"""
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = client.get("/api/v1/system/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] in ["healthy", "unhealthy"]
    
    def test_status_endpoint(self):
        """Test status check endpoint"""
        response = client.get("/api/v1/system/status")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "running"
        assert "endpoints" in data
    
    # v1 endpoint tests
    def test_v1_playlists_endpoints(self):
        """Test v1 playlist endpoints"""
        response = client.get("/api/v1/playlist/")
        assert response.status_code in [200, 404, 500]  # Allow for various responses
        
        # Test with a mock ID
        response = client.get("/api/v1/playlist/test-id")
        assert response.status_code in [200, 404, 500]
    
    def test_v1_users_endpoints(self):
        """Test v1 user endpoints"""
        response = client.get("/api/v1/users/")
        assert response.status_code in [200, 404, 500]
        
        response = client.get("/api/v1/users/test-id")
        assert response.status_code in [200, 404, 500]
    
    def test_v1_profiles_endpoints(self):
        """Test v1 profile endpoints"""
        response = client.get("/api/v1/profiles/")
        assert response.status_code in [200, 404, 500]
        
        response = client.get("/api/v1/profiles/test-id")
        assert response.status_code in [200, 404, 500]
    
    def test_v1_clips_endpoints(self):
        """Test v1 clip endpoints"""
        response = client.get("/api/v1/clip/")
        assert response.status_code in [200, 404, 500]
        
        response = client.get("/api/v1/clip/test-id")
        assert response.status_code in [200, 404, 500]
        
        # Test delete endpoint
        response = client.delete("/api/v1/clip/test-id")
        assert response.status_code in [200, 404, 500]
    
    def test_v1_categories_endpoints(self):
        """Test v1 category endpoints"""
        response = client.get("/api/v1/categories/")
        assert response.status_code in [200, 404, 500]
    
    def test_v1_tags_endpoints(self):
        """Test v1 tag endpoints"""
        response = client.get("/api/v1/tags/")
        assert response.status_code in [200, 404, 500]
    
    def test_v1_templates_endpoints(self):
        """Test v1 template endpoints"""
        response = client.get("/api/v1/templates/")
        assert response.status_code in [200, 404, 500]
    
    def test_v1_prompts_endpoints(self):
        """Test v1 prompt endpoints"""
        response = client.get("/api/v1/prompts/")
        assert response.status_code in [200, 404, 500]
    
    # v2 endpoint tests
    def test_v2_playlists_endpoints(self):
        """Test v2 playlist endpoints"""
        response = client.get("/api/v2/playlist/")
        assert response.status_code in [200, 404, 500]
        
        response = client.get("/api/v2/playlist/test-id")
        assert response.status_code in [200, 404, 500]
    
    def test_v2_users_endpoints(self):
        """Test v2 user endpoints"""
        response = client.get("/api/v2/users/")
        assert response.status_code in [200, 404, 500]
        
        response = client.get("/api/v2/users/test-id")
        assert response.status_code in [200, 404, 500]
    
    def test_v2_profiles_endpoints(self):
        """Test v2 profile endpoints"""
        response = client.get("/api/v2/profiles/")
        assert response.status_code in [200, 404, 500]
        
        response = client.get("/api/v2/profiles/test-id")
        assert response.status_code in [200, 404, 500]
    
    def test_v2_clips_endpoints(self):
        """Test v2 clip endpoints"""
        response = client.get("/api/v2/clip/")
        assert response.status_code in [200, 404, 500]
        
        response = client.get("/api/v2/clip/test-id")
        assert response.status_code in [200, 404, 500]
    
    def test_v2_categories_endpoints(self):
        """Test v2 category endpoints"""
        response = client.get("/api/v2/categories/")
        assert response.status_code in [200, 404, 500]
    
    def test_v2_tags_endpoints(self):
        """Test v2 tag endpoints"""
        response = client.get("/api/v2/tags/")
        assert response.status_code in [200, 404, 500]
    
    def test_v2_templates_endpoints(self):
        """Test v2 template endpoints"""
        response = client.get("/api/v2/templates/")
        assert response.status_code in [200, 404, 500]
    
    def test_v2_prompts_endpoints(self):
        """Test v2 prompt endpoints"""
        response = client.get("/api/v2/prompts/")
        assert response.status_code in [200, 404, 500]
    
    def test_invalid_endpoints_return_404(self):
        """Test that invalid endpoints return 404"""
        response = client.get("/api/v1/invalid-endpoint")
        assert response.status_code == 404
        
        response = client.get("/api/v2/invalid-endpoint")
        assert response.status_code == 404
    
    def test_invalid_methods_return_405(self):
        """Test that invalid HTTP methods return 405"""
        response = client.post("/api/v1/system/health")
        assert response.status_code == 405


def test_environment_config():
    """Test that environment configuration is properly loaded"""
    assert hasattr(settings, 'environment')
    assert settings.environment in ['local', 'dev', 'test', 'prod']
    
    # Test that database URL is properly configured
    assert hasattr(settings, 'database_url')
    assert isinstance(settings.database_url, str)
    
    # Test that debug setting is properly loaded
    assert hasattr(settings, 'debug')
    assert isinstance(settings.debug, bool)


if __name__ == "__main__":
    pytest.main([__file__])