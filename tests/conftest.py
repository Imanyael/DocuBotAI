"""
Pytest configuration and fixtures for DocuBotAI tests.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import os
import json

from docubotai.api.main import app
from docubotai.core.database import get_db, Base
from docubotai.core.config import settings

# Test database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="session")
def test_db_engine():
    """Create test database engine."""
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    return engine

@pytest.fixture(scope="function")
def db_session(test_db_engine):
    """Create database session for testing."""
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_db_engine
    )
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()

@pytest.fixture(scope="function")
def client(db_session):
    """Create FastAPI test client."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture(scope="session")
def test_data():
    """Load test data from fixtures."""
    fixtures_path = os.path.join(
        os.path.dirname(__file__),
        "fixtures",
        "sample_docs.json"
    )
    with open(fixtures_path) as f:
        return json.load(f)

@pytest.fixture(scope="function")
def admin_headers():
    """Create admin headers with API key."""
    return {"X-API-Key": settings.ADMIN_API_KEY}