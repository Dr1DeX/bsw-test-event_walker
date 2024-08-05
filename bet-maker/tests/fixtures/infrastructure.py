import pytest_asyncio

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.infrastructure.database import Base
from tests.fixtures.settings import Settings

settings = Settings()

engine = create_async_engine(
    url=settings.db_url,
    echo=True, future=True,
    pool_pre_ping=True
)

AsyncSessionFactory = async_sessionmaker(
    engine,
    autocommit=False,
    expire_on_commit=False
)


@pytest_asyncio.fixture(scope='session', autouse=True)
async def init_db(event_loop):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope='session')
async def get_db_session():
    yield AsyncSessionFactory()
