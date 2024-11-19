from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError

from schemas.data_fonte_schema import DataFonteSchema
from core.deps import get_session_Fonte

from models.data_fonte_model import DataFonteModel

router = APIRouter()

@router.get('/', response_model=List[DataFonteSchema])
async def get_data(start: datetime, end: datetime, 
                   variables: Optional[str] = None, #ambient_temperature,wind_speed,power
                   db: AsyncSession = Depends(get_session_Fonte)):

        async with db as session:
            try:
                # Para cada variável solicitada, verifica se existe no objeto Data
                # Retorna os dados filtrados, onde cada variável é um campo
                if variables:
                    allowed_variables = set(variables.split(","))
                    print(f"Variáveis recebidas: {allowed_variables}")  # Para debug

                    columns = set(DataFonteModel.__table__.columns.keys())
                    print(f"Colunas válidas no banco: {columns}")  # Para debug

                    invalid_columns = allowed_variables - columns
                    if invalid_columns:
                        raise HTTPException(status_code=400, detail=f"Colunas inválidas: {', '.join(invalid_columns)}")

                    # Adicionar filtros de variáveis na consulta
                    selected_columns = []
                    selected_columns.append(DataFonteModel.id)
                    selected_columns.append(DataFonteModel.timestamp)
                    if 'wind_speed' in allowed_variables:
                        selected_columns.append(DataFonteModel.wind_speed)
                    if 'power' in allowed_variables:
                        selected_columns.append(DataFonteModel.power)
                    if 'ambient_temperature' in allowed_variables:
                        selected_columns.append(DataFonteModel.ambient_temperature)

                    # Usar *args para passar as colunas selecionadas como argumentos separados
                    query = select(DataFonteModel).with_only_columns(*selected_columns).where(DataFonteModel.timestamp.between(start, end))
                    #query = query.with_only_columns([col for col in DataFonteModel.__table__.columns if col.name != 'power'])
                    print(query)
                    result = await session.execute(query)
                    datas: List[DataFonteModel] = result.fetchall()
                    print(datas)
                else:
                    query = select(DataFonteModel).where(DataFonteModel.timestamp.between(start, end))
                    result = await session.execute(query)
                    datas: List[DataFonteModel] = result.scalars().unique().all()

                if datas: 
                    return datas    
                else:
                    raise HTTPException(detail='Valores não encontradas.', status_code=status.HTTP_404_NOT_FOUND)
            except SQLAlchemyError as e:
                # Captura erros do SQLAlchemy e retorna uma mensagem genérica
                raise HTTPException(status_code=500, detail="Erro ao consultar o banco de dados. Detalhes: " + str(e))     
            except Exception as e:
                print(f"Erro ao buscar os dados: {e}")
            
            