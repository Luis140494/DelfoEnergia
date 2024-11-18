from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession
from core.configs import settings

engine_fonte: AsyncEngine = create_async_engine(settings.DB_URL_FONTE)

Session_fonte: AsyncSession = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
    bind=engine_fonte
)

engine_alvo: AsyncEngine = create_async_engine(settings.DB_URL_ALVO)

Session_alvo: AsyncSession = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
    bind=engine_alvo
)