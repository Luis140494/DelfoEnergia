from sqlalchemy import String
from pydantic import BaseModel as SCBaseModel
from typing import Optional
from typing import List
from schemas.data_alvo_schema import DataAlvoSchema

class SignalFonteSchema(SCBaseModel):
    id: Optional[int] = None  
    name: String

class UsuarioSchemaArtigos(SignalFonteSchema):
    artigos: Optional[List[DataAlvoSchema]]
