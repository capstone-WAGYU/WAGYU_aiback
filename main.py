from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils.ask import askRequest, askResponse
from llama_cpp import Llama
import sqlite3

conn = sqlite3.connect('userinfo.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS userinfo (
            userid INTEGER PRIMARY KEY AUTOINCREMENT,
            species TEXT,
            name TEXT,
            age INTEGER,
            disease TEXT)
'''); conn.commit()

APP = FastAPI()
APP.add_middleware(
    CORSMiddleware,
    allow_origins= ["*"],
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*']
)
LLM = Llama(
    model_path="./model/qwen2.5_merged-q4_k_m.gguf", 
    n_ctx = 4096, 
    n_gpu_layers= -1
)
@APP.get("/")
def health():
    return {"status":"ok"}

@APP.post("/ai/ask", response_model=askResponse)
async def ask(req: askRequest):
    pipeline = LLM(
        req.text, max_tokens = 512, temperature= 0.5, top_p = 0.9
        ); answer = pipeline['choices'][0]['text'].strip()
    return askResponse(text = answer)

@APP.get("/ai/info")
def getinfo(userid: int, species: str, name: str, age: int, disease: str):

    conn.execute('''
INSERT INTO userinfo (userid, species, name, age, disease) VALUES (?, ?, ?, ?, ?)'''); conn.commit()

    return {'user': userid, 'species': species, 'name': name, 'age': age, 'disease': disease}
