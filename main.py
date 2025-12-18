from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils.ask import askRequest, askResponse
from utils.threadupdate import threadUpdate
from prompt.prompt import bbobbi_prompt
from llama_cpp import Llama

APP = FastAPI()
APP.add_middleware(
    CORSMiddleware,
    allow_origins= ["*"],
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*']
)
LLM = Llama(
    model_path="./models/capstone-q4-k-m.gguf", 
    n_ctx = 4096, 
    n_gpu_layers= 24,
    verbose = True, 
    chat_format= 'qwen2'
)

@APP.get("/")
def health():
    return {"status":"ok"}

@APP.post("/ai/ask", response_model=askResponse)
async def ask(req: askRequest):
    PROMPT = bbobbi_prompt(req.userid, req.text)
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