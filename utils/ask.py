from pydantic import BaseModel
class askRequest(BaseModel):
    userid: str
    text: str

class askResponse(BaseModel):
    userid: str
    text: str