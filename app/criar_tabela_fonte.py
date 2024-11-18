from core.configs import settings
from core.database import engine_fonte
from datetime import datetime, timedelta
from models.data_fonte_model import DataFonteModel
import random
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import create_async_engine
from core.configs import settings

async def create_tables() -> None:
    import models.__all_models_Fonte
    print('Criar tabela do banco de dados fonte...')

    async with engine_fonte.begin() as conn:
        await conn.run_sync(settings.DBBaseModel.metadata.drop_all)
        await conn.run_sync(settings.DBBaseModel.metadata.create_all)
        print('Tabela criada com sucesso...')
        
def generate_random_data():
    wind_speed = round(random.uniform(0, 100), 2)  # velocidade do vento entre 0 e 100
    power = round(random.uniform(0, 5000), 2)      # potência entre 0 e 5000
    ambient_temperature = round(random.uniform(-30, 50), 2)  # temperatura ambiente entre -30 e 50 graus Celsius
    return wind_speed, power, ambient_temperature

async def populate_database():
    engine_fonte = create_async_engine(settings.DB_URL_FONTE)
    print("Populando o banco de dados com dados aleatórios...")

    start_time = datetime.now() - timedelta(days=10)  # 10 dias atrás
    end_time = datetime.now()
    time_interval = timedelta(minutes=1)
        
    while start_time <= end_time:
        async with engine_fonte.begin() as conn:
            try:
                wind_speed, power, ambient_temperature = generate_random_data()
                await conn.execute(insert(DataFonteModel).values(
                                                timestamp=start_time,
                                                wind_speed=wind_speed,
                                                power=power,
                                                ambient_temperature=ambient_temperature
                                            ))
                start_time += time_interval
                
                await conn.commit()
                await conn.close()

                    # Log da inserção
                print(f"Inserido: {start_time} | Vento: {wind_speed} | Potência: {power} | Temp: {ambient_temperature}")
            except Exception as e:
                print(f"Erro na inserção de dados: {e}")
                await conn.rollback()

                    # Incrementar o timestamp para o próximo minuto
            start_time += timedelta(minutes=1)

            # Esperar 1 minuto antes de inserir o próximo conjunto de dados
            await asyncio.sleep(60)

        
    
if __name__ == '__main__':
    import asyncio
    import warnings

    warnings.filterwarnings("ignore", category=DeprecationWarning)
    asyncio.run(create_tables())
    
    asyncio.run(populate_database())
