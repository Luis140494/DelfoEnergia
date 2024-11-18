from sqlalchemy import Column, Float, Integer, DateTime
from core.configs import settings

class DataFonteModel(settings.DBBaseModel):
    __tablename__ = 'data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False)  
    wind_speed = Column(Float, nullable=False, default=0)  
    power = Column(Float, nullable=False, default=0) 
    ambient_temperature = Column(Float, nullable=False, default=0) 

