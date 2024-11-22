import asyncio
from collections.abc import AsyncGenerator, Generator
from functools import wraps
from unittest import mock
from unittest.mock import AsyncMock

import pytest
import pytest_asyncio
import sqlalchemy
from httpx import ASGITransport, AsyncClient
from sqlalchemy import Result, sql
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from pytest_mock import MockerFixture
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend


from api.services.trade import TradeService
import config
from models.base import BaseModel
from tests.fixtures.fake_service import FakeTradeService
# from main import app


@pytest.fixture(scope="session")
def event_loop(request: pytest.FixtureRequest) -> asyncio.AbstractEventLoop:
    """Returns a new event_loop."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def create_test_db() -> None:
    """Creates a test base for the duration of the tests."""
    assert config.MODE == "TEST"

    sqlalchemy_database_url = (
        f"postgresql+asyncpg://{config.DB_USER}:{config.DB_PASS}"
        f"@{config.DB_HOST}:{config.DB_PORT}/"
    )
    nodb_engine = create_async_engine(
        sqlalchemy_database_url,
        echo=False,
        future=True,
    )
    db = AsyncSession(bind=nodb_engine)

    db_exists_query = sql.text(
        f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{config.DB_NAME}'"
    )
    db_exists: Result = await db.execute(db_exists_query)
    db_exists = db_exists.fetchone() is not None
    autocommit_engine = nodb_engine.execution_options(isolation_level="AUTOCOMMIT")
    connection = await autocommit_engine.connect()
    if not db_exists:
        db_create_query = sql.text(f"CREATE DATABASE {config.DB_NAME}")
        await connection.execute(db_create_query)

    yield

    db_drop_query = sql.text(f"DROP DATABASE IF EXISTS {config.DB_NAME} WITH (FORCE)")
    await db.close()
    await connection.execute(db_drop_query)
    await connection.close()
    await nodb_engine.dispose()


@pytest_asyncio.fixture(scope="session")
async def db_engine(create_test_db: None) -> AsyncGenerator[AsyncEngine, None]:
    """Returns the test Engine."""
    DB_URL = f"postgresql+asyncpg://{config.DB_USER}:{config.DB_PASS}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}"
    engine = create_async_engine(
        DB_URL,
        echo=False,
        future=True,
        pool_size=50,
        max_overflow=100,
    ).execution_options(compiled_cache=None)

    yield engine

    await engine.dispose()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_schemas(db_engine: AsyncEngine) -> None:
    """Creates schemas in the test database."""
    assert config.MODE == "TEST"

    schemas = ("oil_trades",)

    async with db_engine.connect() as conn:
        for schema in schemas:
            await conn.execute(sqlalchemy.schema.CreateSchema(schema))
            await conn.commit()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_db(db_engine: AsyncEngine, setup_schemas: None) -> None:
    """Creates tables in the test database and insert needs data."""
    assert config.MODE == "TEST"

    async with db_engine.begin() as db_conn:
        await db_conn.run_sync(BaseModel.metadata.drop_all)
        await db_conn.run_sync(BaseModel.metadata.create_all)


@pytest_asyncio.fixture
async def transaction_session(
    db_engine: AsyncEngine,
) -> AsyncGenerator[AsyncSession, None]:
    """Returns a connection to the database.
    Any changes made to the database will NOT be applied, only for the duration of the TestCase.
    """
    connection = await db_engine.connect()
    await connection.begin()
    session = AsyncSession(bind=connection)

    yield session

    await session.rollback()
    await connection.close()


@pytest_asyncio.fixture
def fake_trade_service(
    transaction_session: AsyncSession,
) -> Generator[FakeTradeService, None]:
    _fake_trade_service = FakeTradeService(transaction_session)
    yield _fake_trade_service
    
def mock_cache(*args, **kwargs):
    def wrapper(func):
        @wraps(func)
        async def inner(*args, **kwargs):
            return await func(*args, **kwargs)

        return inner

    return wrapper


mock.patch("fastapi_cache.decorator.cache", mock_cache).start()
    


@pytest_asyncio.fixture
async def async_client(
    fake_trade_service: FakeTradeService,
) -> AsyncGenerator[AsyncClient, None]:
    from main import app
    app.dependency_overrides[TradeService] = lambda: fake_trade_service

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac