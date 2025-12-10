from fastapi import FastAPI
from utils.ask import askRequest, askResponse
from utils.getinfos import getinfo
from prompt.prompt import bbobbi_prompt
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
def getinfo(species, name, age, disease):
    return {"species": species, "name": name, "age": age, "disease": disease}