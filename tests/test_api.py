"""
Tests for DocuBotAI API endpoints.
"""
import pytest
from fastapi.testclient import TestClient

def test_root_endpoint(client: TestClient):
    """Test root endpoint returns correct information."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "DocuBotAI"
    assert "version" in data
    assert data["status"] == "operational"

def test_health_check(client: TestClient):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_create_tool(client: TestClient):
    """Test tool creation endpoint."""
    tool_data = {
        "name": "Test Tool",
        "description": "A test tool",
        "url": "https://test.com",
        "category": "testing"
    }
    response = client.post("/tools/", json=tool_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == tool_data["name"]
    assert data["description"] == tool_data["description"]
    assert data["url"] == tool_data["url"]
    assert data["category"] == tool_data["category"]

def test_create_scraping_task(client: TestClient):
    """Test scraping task creation."""
    task_data = {
        "url": "https://docs.test.com",
        "max_depth": 2,
        "include_patterns": ["*.md"],
        "exclude_patterns": ["*test*"]
    }
    response = client.post("/scraping/", json=task_data)
    assert response.status_code == 200
    data = response.json()
    assert data["url"] == str(task_data["url"])
    assert data["status"] == "pending"

def test_query_documents(client: TestClient):
    """Test RAG query endpoint."""
    query_data = {
        "text": "How to use the test tool?",
        "context": "testing",
        "max_results": 5,
        "min_similarity": 0.7
    }
    response = client.post("/query/", json=query_data)
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "sources" in data
    assert "confidence" in data
    assert "execution_time" in data

def test_admin_status(client: TestClient, admin_headers):
    """Test admin status endpoint with authentication."""
    response = client.get("/admin/status", headers=admin_headers)
    assert response.status_code == 200
    data = response.json()
    assert "cpu_usage" in data
    assert "memory_usage" in data
    assert "disk_usage" in data
    assert "active_tasks" in data
    assert "queue_size" in data
    assert "uptime" in data

def test_admin_status_unauthorized(client: TestClient):
    """Test admin status endpoint without authentication."""
    response = client.get("/admin/status")
    assert response.status_code == 403

def test_maintenance_mode(client: TestClient, admin_headers):
    """Test maintenance mode functionality."""
    # Enable maintenance mode
    response = client.post(
        "/admin/maintenance",
        headers=admin_headers,
        json={"enabled": True, "message": "Under maintenance"}
    )
    assert response.status_code == 200
    
    # Try to access protected endpoint
    response = client.get("/tools/")
    assert response.status_code == 503
    assert "Under maintenance" in response.json()["detail"]
    
    # Health check should still work
    response = client.get("/health")
    assert response.status_code == 200
    
    # Disable maintenance mode
    response = client.post(
        "/admin/maintenance",
        headers=admin_headers,
        json={"enabled": False}
    )
    assert response.status_code == 200