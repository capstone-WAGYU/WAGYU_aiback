from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from utils.ask import askRequest, askResponse
from utils.threadupdate import threadUpdate
from prompt.prompt import bbobbi_prompt
from llama_cpp import Llama
import os

LLM = None
@asynccontextmanager
async def lifesp(APP = FastAPI):
    global LLM
    MODEL_PATH = os.getenv("MODEL_PATH")
    if not MODEL_PATH: raise RuntimeError("모델 경로 환경변수 없는듯")
    LLM = Llama(model_path=MODEL_PATH, n_ctx = 4096, n_gpu_layers=24, verbose = True, chat_format = 'qwen2')
    yield

    LLM = None

APP = FastAPI(lifespan=lifesp)
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
async def ask(req):
    PROMPT = bbobbi_prompt(req.text)
    out = LLM.create_chat_completion(
        messages=[{"role": "system", 'content': PROMPT},
            {"role": "user", "content": req.text}],
        temperature=0.3,
        top_p=0.9,
        max_tokens=512,
        stop = ["<|im_end|>"],
    )
    answer = out["choices"][0]["message"]["content"].strip()
    print("RAW:", repr(req.text))
    print(type(out))
    print(out)
    print(type(answer))
    print(answer[:200])

    return askResponse(userid=req.userid, text=answer)