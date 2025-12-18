from pydantic import BaseModel
from typing import Optional
class askRequest(BaseModel):
    userid: str
    species: str
    text: str

class askResponse(BaseModel):
    userid: Optional[str] = None
    text: str