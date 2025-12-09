from pydantic import BaseModel
class askRequest(BaseModel):
    text: str

class askResponse(BaseModel):
    text: str