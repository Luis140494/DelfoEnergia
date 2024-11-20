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

@router.get('/')
async def get_data(start: datetime, end: datetime, 
                   variables: Optional[str] = None, #ambient_temperature,wind_speed,power
                   db: AsyncSession = Depends(get_session_Fonte)):

        async with db as session:
            try:
                query = select(DataFonteModel).where(DataFonteModel.timestamp.between(start, end))
                result = await session.execute(query)
                datas: List[DataFonteModel] = result.scalars().unique().all()
                if datas:
                    if variables:
                        allowed_variables = set(variables.split(","))
                        print(f"Variáveis recebidas: {allowed_variables}")  # Para debug

                        columns = set(DataFonteModel.__table__.columns.keys())
                        print(f"Colunas válidas no banco: {columns}")  # Para debug

                        invalid_columns = allowed_variables - columns
                        if invalid_columns:
                            raise HTTPException(status_code=400, detail=f"Colunas inválidas: {', '.join(invalid_columns)}")

                        filtered_data = []
                        for row in datas:
                            data_row = {var: getattr(row, var) for var in variables if hasattr(row, var)}
                            
                            data_row["id"] = row.id
                            data_row["timestamp"] = row.timestamp

                            if 'wind_speed' in allowed_variables:
                                data_row["wind_speed"] = row.wind_speed

                            if 'power' in allowed_variables:
                                data_row["power"] = row.wind_speed

                            if 'ambient_temperature' in allowed_variables:
                                data_row["ambient_temperature"] = row.wind_speed
                            
                            filtered_data.append(data_row)

                        #data_model_instances = [DataFonteModel(**entry) for entry in filtered_data]
                        print(filtered_data)
                        return filtered_data
                    else:
                       return datas     
                else:
                    raise HTTPException(detail='Valores não encontradas.', status_code=status.HTTP_404_NOT_FOUND)
            except SQLAlchemyError as e:
                # Captura erros do SQLAlchemy e retorna uma mensagem genérica
                raise HTTPException(status_code=500, detail="Erro ao consultar o banco de dados. Detalhes: " + str(e))     
            except Exception as e:
                print(f"Erro ao buscar os dados: {e}")
            
            