from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from schemas.data_fonte_schema import DataFonteSchema
from core.deps import get_session_Fonte

from models.data_fonte_model import DataFonteModel

router = APIRouter()

@router.get('/', response_model=List[DataFonteSchema])
async def get_data(start: datetime, end: datetime, 
                   variables: Optional[List[str]] = Query([]), #variables=power&variables=wind_speed&variables=ambient_temperature 
                   db: AsyncSession = Depends(get_session_Fonte)):

        async with db as session:
            try:
                query = select(DataFonteModel).where(DataFonteModel.timestamp.between(start, end))
                # Para cada variável solicitada, verifica se existe no objeto Data
                # Retorna os dados filtrados, onde cada variável é um campo
                if variables:
                    columns = [getattr(DataFonteModel, var) for var in variables if hasattr(DataFonteModel, var)]
                    query = query.with_only_columns(*columns)
                    
                result = await session.execute(query)
                datas: List[DataFonteModel] = result.scalars().unique().all()
                if datas: 
                    return datas    
                else:
                    raise HTTPException(detail='Valores não encontradas.', status_code=status.HTTP_404_NOT_FOUND)     
            except Exception as e:
                print(f"Erro ao buscar os dados: {e}")
            