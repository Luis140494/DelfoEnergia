from pydantic import BaseModel as SCBaseModel
from typing import Optional
from datetime import datetime
from sqlmodel import Field


class DataFonteSchema(SCBaseModel):
    id: Optional[int]
    timestamp: Optional[datetime]   
    wind_speed: Optional[float]
    power: Optional[float] 
    ambient_temperature: Optional[float]

    class Config:
        orm_mode = True