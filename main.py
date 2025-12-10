from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils.ask import askRequest, askResponse
APP = FastAPI()

APP.add_middleware(
    CORSMiddleware,
    allow_origins= ["*"],
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*']
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
