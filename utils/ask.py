from pydantic import BaseModel
from typing import Optional, List
class askRequest(BaseModel):
    userid: Optional[str] = None
    species: str
    name: str
    age: int
    disease: List[str]
    text: str

class askResponse(BaseModel):
    userid: Optional[str] = None
    text: str