from core.configs import settings
from core.database import engine_alvo

async def create_tables() -> None:
    import models.__all_models_Alvo
    print('Criar tabela do banco de dados Alvo...')

    async with engine_alvo.begin() as conn:
        await conn.run_sync(settings.DBBaseModel.metadata.drop_all)
        await conn.run_sync(settings.DBBaseModel.metadata.create_all)
    print('Tabelas criadas com sucesso...')

if __name__ == '__main__':
    import asyncio
    import warnings

    warnings.filterwarnings("ignore", category=DeprecationWarning)
    asyncio.get_event_loop().run_until_complete(create_tables())
    