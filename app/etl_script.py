import httpx
import pandas as pd
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import insert
from core.configs import settings
from datetime import date
from models.data_alvo_model import DataAlvoModel # Aqui você define o modelo SQLAlchemy
from models.signal_alvo_model import SignalAlvoModel # Aqui você define o modelo SQLAlchemy


async def fetch_data_from_api(start_date: date, end_date: date, variables: list[str]):
    try:
        url_api = f"http://localhost:8000/api/v1/data/?start={start_date}T00:00:00.00&end={end_date}T23:59:59.00"
        list_variables = ''
        for var in variables:
            list_variables = list_variables + '&variables=' + f'"{var}"'

        url_api = url_api + list_variables
        url_api = url_api.replace(" ", "")
        print(url_api)
        async with httpx.AsyncClient() as client:
            response = await client.get(url_api)
            data = response.json()
            return data
    except Exception as e:
        print(f"Erro ao decodificar a resposta JSON: {e}")
        return None

async def process_and_insert_data(data):
    engine_alvo = create_async_engine(settings.DB_URL_ALVO)
    df = pd.DataFrame(data)
    if 'timestamp' not in df.columns:
        print("Erro: A coluna 'timestamp' não está presente nos dados recebidos.")
        return  # Encerra a função se a coluna 'timestamp' não estiver presente
    
    # Se a coluna 'timestamp' existir, converte para datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

    # Verifique se houve falha na conversão para datetime
    if df['timestamp'].isnull().any():
        print("Erro: Algumas datas não puderam ser convertidas corretamente.")
        print(df[df['timestamp'].isnull()])  # Exibe as linhas com erro de conversão
        return
    
    # Define 'timestamp' como o índice
    df.set_index('timestamp', inplace=True)
    # Agrega os dados 10-minutais com a função 'resample'
    try:
        df_resampled = df.resample('10min').agg({
            'wind_speed': ['mean', 'min', 'max', 'std'],
            'power': ['mean', 'min', 'max', 'std']
        })
    except Exception as e:
        print(f"Erro durante o resample: {e}")
        return

    # Processar os dados para inserção no banco alvo
    for timestamp, row in df_resampled.iterrows():
            try:
                async with engine_alvo.begin() as conn:
                    signal = SignalAlvoModel
                    querySignal = insert(signal).values(name="wind_speed").returning(signal.id)
                    result = await conn.execute(querySignal)
                    signal_id = result.scalar()
                    await conn.commit()
                    await conn.close()

                for variable in ['wind_speed', 'power']:
                    for agg in ['mean', 'min', 'max', 'std']:
                        async with engine_alvo.begin() as conn:
                            data = DataAlvoModel
                            queryData = insert(data).values(timestamp=timestamp, signal_id=signal_id, 
                                                            value=row[(variable, agg)])
                            result = await conn.execute(queryData)
                            await conn.commit()
                            await conn.close()
            
            except Exception as e:
                print(f"Erro: {e}")
                await conn.rollback()
                raise   

    

async def etl_pipeline(start_date: date, end_date: date, variables: list[str]):
    data = await fetch_data_from_api(start_date, end_date, variables)
    await process_and_insert_data(data)

if __name__ == "__main__":
    start_date = date(2024, 11, 5)
    end_date = date(2024, 11, 22)
    asyncio.run(etl_pipeline(start_date, end_date, ['wind_speed', 'power']))
