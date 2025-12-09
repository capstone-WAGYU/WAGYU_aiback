from fastapi import FastAPI
from utils.ask import askRequest, askResponse
from utils.getinfos import getinfo
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
def getinfo(req: getinfo):
    # API명세서 보고 진행
    pass
