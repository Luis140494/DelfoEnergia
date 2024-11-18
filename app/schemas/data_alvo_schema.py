from sqlalchemy import Float
from pydantic import BaseModel as SCBaseModel
from typing import Optional
from datetime import datetime

class DataAlvoSchema(SCBaseModel):
    id: Optional[int] = None
    timestamp = datetime 
    value = Float 
    id_signal: Optional[int]

    class Config:
        orm_mode = True