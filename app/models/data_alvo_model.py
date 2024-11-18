from sqlalchemy import Column, Float, Integer, DateTime, ForeignKey
from core.configs import settings
from sqlalchemy.orm import relationship 


class DataAlvoModel(settings.DBBaseModel):
    __tablename__ = "data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False)
    value = Column(Float, nullable=False)  
    signal_id = Column(Integer, ForeignKey('signals.id'))
    signal = relationship("SignalAlvoModel", back_populates='data', lazy='joined')