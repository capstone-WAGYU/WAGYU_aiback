from pydantic import BaseModel

class getinfo(BaseModel):
    species: str
    name: str
    age: int
    disease: str