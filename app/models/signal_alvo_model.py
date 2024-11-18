from sqlalchemy import Integer, String, Column
from sqlalchemy.orm import relationship
from core.configs import settings

class SignalAlvoModel(settings.DBBaseModel):
    __tablename__ = "signals"

    id = Column(Integer, primary_key=True, autoincrement=True)  
    name = Column(String(256), nullable=False)  
    data = relationship(
        "DataAlvoModel",
        cascade="all,delete-orphan",
        back_populates="signal",
        uselist=True,
        lazy="joined"
    )