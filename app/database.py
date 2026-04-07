"""SQLAlchemy async engine and session factory.

Usage:
    from app.database import get_session

    async def my_endpoint(session: AsyncSession = Depends(get_session)):
        ...
"""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import settings

engine = create_async_engine(
    settings.database_url,
    echo=False,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)

async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency that yields an async DB session.

    Endpoints are responsible for calling ``await session.commit()`` when
    they have made changes that should be persisted. On any unhandled
    exception the session is rolled back automatically.
    """
    async with async_session_factory() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
