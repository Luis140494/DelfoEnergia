from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import column

from schemas.data_fonte_schema import DataFonteSchema
from core.deps import get_session_Fonte

from models.data_fonte_model import DataFonteModel

router = APIRouter()

@router.get('/', response_model=List[DataFonteSchema])
async def get_data(start: datetime, end: datetime, 
                   variables: Optional[List[str]] = Query([]), #ambient_temperature,wind_speed,power
                   db: AsyncSession = Depends(get_session_Fonte)):

        async with db as session:
            try:
                # Para cada variável solicitada, verifica se existe no objeto Data
                # Retorna os dados filtrados, onde cada variável é um campo
                if variables:
                    colunas_desejadas = variables[0].split(',')
                    colunas_para_selecionar = [
                                    getattr(DataFonteModel, coluna) 
                                    for coluna in colunas_desejadas 
                                    if hasattr(DataFonteModel, coluna)]
        
                    query = select(DataFonteModel).where(DataFonteModel.timestamp.between(start, end)).with_only_columns(*colunas_para_selecionar)
                else:
                    query = select(DataFonteModel).where(DataFonteModel.timestamp.between(start, end))  

                result = await session.execute(query)
                datas: List[DataFonteModel] = result.scalars().unique().all()
                if datas: 
                    return datas    
                else:
                    raise HTTPException(detail='Valores não encontradas.', status_code=status.HTTP_404_NOT_FOUND)     
            except Exception as e:
                print(f"Erro ao buscar os dados: {e}")
            