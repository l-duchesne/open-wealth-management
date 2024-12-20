import pytest
import pytest_asyncio
from app.main import app
from app.models.db.database import get_db
from app.models.db.item import Base
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Create a test database
DATABASE_URL = "sqlite+aiosqlite:///:memory:"
engine = create_async_engine(DATABASE_URL, future=True)
TestSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


# Override the get_db dependency to use the test database
async def override_get_db():
    async with TestSessionLocal() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db


@pytest_asyncio.fixture(scope="module")
async def setup_database():
    # Create the tables in the test database
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Drop the tables after tests
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="module")
async def test_client(setup_database):  # Ensure the database setup runs first
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client


@pytest.mark.asyncio
async def test_read_root(test_client: AsyncClient):
    response = await test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to My API!"}


@pytest.mark.asyncio
async def test_create_item(test_client: AsyncClient, setup_database):
    # setup_database runs first; test_client uses it
    item_data = {
        "name": "Test Item",
        "description": "This is a test item",
        "price": 9.99,
        "in_stock": True
    }
    response = await test_client.post("/items/", json=item_data)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["name"] == "Test Item"
    assert response_data["price"] == 9.99
    assert response_data["in_stock"] is True


@pytest.mark.asyncio
async def test_get_items(test_client: AsyncClient, setup_database):
    response = await test_client.get("/items/")
    assert response.status_code == 200
    items = response.json()
    assert len(items) == 1
    assert items[0]["name"] == "Test Item"
    assert items[0]["price"] == 9.99
