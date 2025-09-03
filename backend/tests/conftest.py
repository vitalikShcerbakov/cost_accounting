import pytest
import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from main import app
from database import Base, get_db

# URL-адрес базы данных SQLite для тестирования
SQLITE_DATABASE_URL = "sqlite:///./test_db.db"

# Create a SQLAlchemy engine
engine = create_engine(
 SQLITE_DATABASE_URL,
 connect_args={"check_same_thread": False},
 poolclass=StaticPool,
)

# Create a sessionmaker to manage sessions
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables in the database
Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Create a new database session with a rollback at the end of the test."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")  #
def test_client(db_session):
    def override_get_db():
        try:
            yield db_session
        except Exception:
            pass
        finally:
            db_session.close()
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture()
def user_payload(): # user_id
    """Generate an updated user payload."""
    return {
          "id": 0,
          "name": "string",
          "email": "user@example.com",
          "is_active": True,
          "password": "string"
    }

@pytest.fixture()
def user_payload_token(): # user_id
    """Generate an updated user payload."""
    return {
          "name": "string",
          "password": "string"
    }