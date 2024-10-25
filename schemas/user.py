from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    id: Optional[int]  # El id es opcional y solo estará presente en las respuestas
    name: str
    email: str
    password: str