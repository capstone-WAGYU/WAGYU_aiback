from fastapi import FastAPI
from utils.ask import askRequest, askResponse
APP = FastAPI()

APP.middleware(
    middleware_type='CORS'
)
@APP.get("/")
def health():
    return {"status":"ok"}

@APP.post("/ai/ask", response_model=askResponse)
async def ask(req: askRequest):
    return askResponse(text=req.text)

@APP.get("/ai/info")
def getinfo(userid: str, species: str, name: str, age: int, disease: str):
    return {'user': userid, 'species': species, 'name': name, 'age': age, 'disease': disease}
