from pydantic.v1 import BaseSettings
from sqlalchemy.ext.declarative import declarative_base

class Settings(BaseSettings):
    """
    Configurações gerais usadas na aplicação
    """
    API_V_STR: str = '/api/v1'
    DB_URL_FONTE: str = 'postgresql+asyncpg://delfo:teste123@localhost:5432/Fonte'
    DB_URL_ALVO: str = 'postgresql+asyncpg://delfo:teste123@localhost:5432/Alvo'
    DBBaseModel = declarative_base()

    class Config:
        case_sensitive = True

settings = Settings()
