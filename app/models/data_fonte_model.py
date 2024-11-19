from sqlalchemy import Column, Float, Integer, DateTime
from core.configs import settings

class DataFonteModel(settings.DBBaseModel):
    __tablename__ = 'data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False)  
    wind_speed = Column(Float, nullable=False, default=0)  
    power = Column(Float, nullable=False, default=0) 
    ambient_temperature = Column(Float, nullable=False, default=0) 

    def __repr__(self):
        return f"<DataFonteModel(id={self.id}, timestamp={self.timestamp}, wind_speed={self.wind_speed}, power={self.power}, ambient_temperature={self.ambient_temperature})>"

