from typing import Generator
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import Session_fonte, Session_alvo

async def get_session_Fonte() -> Generator:
    session_fonte: AsyncSession = Session_fonte()

    try:
        yield session_fonte
    finally:
        await session_fonte.close()

async def get_session_Alvo() -> Generator:
    session_alvo: AsyncSession = Session_alvo()

    try:
        yield session_alvo
    finally:
        await session_alvo.close()